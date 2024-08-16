"""Test the DeterministicStateTransitionModel"""

import numpy as np
import tensorflow as tf

from gemlib.distributions import DeterministicStateTransitionModel


def test_deterministic_dormandprice(homogeneous_sir_params):
    """Test we get a functioning deterministic model using DormandPrince"""

    model_params = homogeneous_sir_params(0.8, 0.14)
    print("model_params:", model_params)
    times = np.arange(0.0, model_params["num_steps"], 1.0, dtype=np.float32)
    del model_params["num_steps"]

    model = DeterministicStateTransitionModel(**model_params, times=times)
    sample = tf.function(lambda: model.sample(), jit_compile=True)()

    assert sample.times.shape == times.shape
    assert sample.states.shape == (199, 1, 3)


def test_deterministic_bdf(homogeneous_sir_params):
    """Test we get a functioning deterministic model using BDF"""

    model_params = homogeneous_sir_params(0.8, 0.14)

    model = DeterministicStateTransitionModel(**model_params, solver="BDF")
    sample = tf.function(lambda: model.sample((2, 3)), jit_compile=True)()

    assert sample.times.shape == (2, 3, 199)
    assert sample.states.shape == (2, 3, 199, 1, 3)


def test_deterministic_log_prob(homogeneous_sir_params):
    """Test log_prob"""

    model_params = homogeneous_sir_params(0.8, 0.14)
    model = DeterministicStateTransitionModel(**model_params)

    sample = model.sample()
    lp = model.log_prob(sample)

    assert lp == 0.0

    lp1 = DeterministicStateTransitionModel(
        **homogeneous_sir_params(1.5, 0.2)
    ).log_prob(sample)

    assert lp1 == -np.inf
