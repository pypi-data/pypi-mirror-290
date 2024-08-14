# -*- coding: utf-8 -*-
"""Test methods related to initialising and resuming the proposal method"""
import numpy as np
import os
import pytest
from unittest.mock import patch, MagicMock

from nessai.proposal import FlowProposal


def test_init(model):
    """Test init with some kwargs"""
    fp = FlowProposal(model, poolsize=1000)
    assert fp.model == model


@pytest.mark.parametrize(
    "value, expected", [(True, True), (False, False), (None, False)]
)
def test_init_use_default_reparams(model, proposal, value, expected):
    """Assert use_default_reparameterisations is set correctly"""
    proposal.use_default_reparameterisations = False
    FlowProposal.__init__(
        proposal, model, poolsize=10, use_default_reparameterisations=value
    )
    assert proposal.use_default_reparameterisations is expected


@pytest.mark.parametrize("ef, fuzz", [(2.0, 3.0**0.5), (False, 2.0)])
def test_initialise(tmpdir, proposal, ef, fuzz):
    """Test the initialise method"""
    p = tmpdir.mkdir("test")
    proposal.initialised = False
    proposal.output = os.path.join(p, "output")
    proposal.rescaled_dims = 2
    proposal.expansion_fraction = ef
    proposal.fuzz = 2.0
    proposal.flow_config = {}
    proposal.training_config = {}
    proposal.set_rescaling = MagicMock()
    proposal.verify_rescaling = MagicMock()
    proposal.update_flow_config = MagicMock()
    proposal.configure_constant_volume = MagicMock()
    fm = MagicMock()
    fm.initialise = MagicMock()
    proposal._FlowModelClass = MagicMock(new=fm)

    FlowProposal.initialise(proposal, resumed=False)

    proposal.set_rescaling.assert_called_once()
    proposal.verify_rescaling.assert_called_once()
    proposal.update_flow_config.assert_called_once()
    proposal.configure_constant_volume.assert_called_once()
    proposal._FlowModelClass.assert_called_once_with(
        flow_config=proposal.flow_config,
        training_config=proposal.training_config,
        output=proposal.output,
    )
    proposal.flow.initialise.assert_called_once()
    assert proposal.populated is False
    assert proposal.initialised
    assert proposal.fuzz == fuzz
    assert os.path.exists(os.path.join(p, "output"))


def test_resume(proposal):
    """Test the resume method."""
    from numpy import array, array_equal

    proposal.initialise = MagicMock()
    proposal.mask = [1, 0]
    proposal.update_bounds = False
    proposal.weights_file = None
    model = MagicMock()
    with patch("nessai.proposal.base.Proposal.resume") as mock:
        FlowProposal.resume(proposal, model, {})
    mock.assert_called_once_with(model)
    proposal.initialise.assert_called_once()
    assert array_equal(proposal.flow_config["mask"], array([1, 0]))


@patch("os.path.exists", return_value=True)
def test_resume_w_weights(osexist, proposal):
    """Test the resume method with weights"""
    proposal.initialise = MagicMock()
    proposal.flow = MagicMock()
    proposal.mask = None
    proposal.update_bounds = False
    proposal.weights_file = None
    model = MagicMock()
    with patch("nessai.proposal.base.Proposal.resume") as mock:
        FlowProposal.resume(proposal, model, {}, weights_file="weights.pt")
    mock.assert_called_once_with(model)
    osexist.assert_called_once_with("weights.pt")
    proposal.initialise.assert_called_once()
    proposal.flow.reload_weights.assert_called_once_with("weights.pt")


@pytest.mark.parametrize("populated", [False, True])
@pytest.mark.parametrize("mask", [None, [1, 0]])
def test_get_state(proposal, populated, mask):
    """Test the get state method used for pickling the proposal.

    Tests cases where the proposal is and isn't populated.
    """

    proposal.populated = populated
    proposal.indices = [1, 2]
    proposal._reparameterisation = MagicMock()
    proposal.model = MagicMock()
    proposal._flow_config = {}
    proposal.initialised = True
    proposal.flow = MagicMock()
    proposal.flow.weights_file = "file"
    proposal._draw_func = lambda x: x

    if mask is not None:
        proposal.flow.flow_config = {"mask": mask}

    state = FlowProposal.__getstate__(proposal)

    assert state["resume_populated"] is populated
    assert state["initialised"] is False
    assert state["weights_file"] == "file"
    assert state["mask"] is mask
    assert "model" not in state
    assert "flow" not in state
    assert "_flow_config" not in state


@pytest.mark.integration_test
@pytest.mark.parametrize("reparameterisation", [False, True])
@pytest.mark.parametrize("init", [False, True])
@pytest.mark.parametrize(
    "latent_prior", ["truncated_gaussian", "uniform_nball", "gaussian"]
)
def test_resume_pickle(model, tmpdir, reparameterisation, init, latent_prior):
    """Test pickling and resuming the proposal.

    Tests both with and without reparameterisations and before and after
    initialise has been called.
    """
    import pickle

    output = tmpdir.mkdir("test_integration")
    if reparameterisation:
        reparameterisations = {"default": {"parameters": model.names}}
    else:
        reparameterisations = None

    if latent_prior != "truncated_gaussian":
        constant_volume_mode = False
    else:
        constant_volume_mode = True

    proposal = FlowProposal(
        model,
        poolsize=1000,
        plot=False,
        expansion_fraction=1,
        output=output,
        reparameterisations=reparameterisations,
        latent_prior=latent_prior,
        constant_volume_mode=constant_volume_mode,
    )
    if init:
        proposal.initialise()

    proposal.mask = None
    proposal.resume_populated = False

    proposal_data = pickle.dumps(proposal)
    proposal_re = pickle.loads(proposal_data)
    proposal_re.resume(model, {})

    assert proposal._plot_pool == proposal_re._plot_pool
    assert proposal._plot_training == proposal_re._plot_training

    if init:
        assert proposal.fuzz == proposal_re.fuzz
        assert proposal.prime_parameters == proposal_re.rescaled_names


def test_reset(proposal):
    """Test reset method"""
    proposal.x = 1
    proposal.samples = 2
    proposal.populated = True
    proposal.populated_count = 10
    proposal._reparameterisation = MagicMock()
    FlowProposal.reset(proposal)
    assert proposal.x is None
    assert proposal.samples is None
    assert proposal.populated is False
    assert proposal.populated_count == 0
    assert proposal.r is np.nan
    assert proposal.alt_dist is None
    assert proposal._checked_population
    proposal._reparameterisation.reset.assert_called_once()


@pytest.mark.timeout(60)
@pytest.mark.integration_test
@pytest.mark.parametrize(
    "latent_prior", ["truncated_gaussian", "uniform_nball", "gaussian"]
)
def test_reset_integration(tmpdir, model, latent_prior):
    """Test reset method iteration with other methods"""
    flow_config = dict(
        n_neurons=1,
        n_blocks=1,
        n_layers=1,
        batch_norm_between_layers=False,
        linear_transform=None,
    )
    training_config = dict(patience=20)
    output = str(tmpdir.mkdir("reset_integration"))
    poolsize = 2
    drawsize = 100
    if latent_prior != "truncated_gaussian":
        constant_volume_mode = False
    else:
        constant_volume_mode = True
    proposal = FlowProposal(
        model,
        output=output,
        flow_config=flow_config,
        training_config=training_config,
        plot=False,
        poolsize=poolsize,
        drawsize=drawsize,
        expansion_fraction=None,
        latent_prior=latent_prior,
        constant_volume_mode=constant_volume_mode,
    )

    modified_proposal = FlowProposal(
        model,
        output=output,
        flow_config=flow_config,
        training_config=training_config,
        plot=False,
        poolsize=poolsize,
        drawsize=drawsize,
        expansion_fraction=None,
        latent_prior=latent_prior,
        constant_volume_mode=constant_volume_mode,
    )
    proposal.initialise()
    modified_proposal.initialise()

    modified_proposal.populate(model.new_point())
    modified_proposal.reset()

    # attributes that should be different
    ignore = [
        "population_time",
        "_reparameterisation",
    ]

    d1 = proposal.__getstate__()
    d2 = modified_proposal.__getstate__()

    for key in ignore:
        d1.pop(key)
        d2.pop(key)

    assert d1 == d2
