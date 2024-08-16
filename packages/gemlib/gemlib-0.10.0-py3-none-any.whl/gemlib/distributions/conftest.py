"""Test fixtures for gemlib.distributions"""

from typing import List, NamedTuple

import numpy as np
import pytest
import tensorflow as tf


class EventList(NamedTuple):
    time: List[float]
    transition: List[int]
    individual: List[int]


@pytest.fixture
def homogeneous_sir_params():
    def fn(beta, gamma):
        def rate_fn(t, state):
            si_rate = beta * state[:, 1] / tf.reduce_sum(state, axis=-1)
            ir_rate = tf.broadcast_to([gamma], si_rate.shape)
            return si_rate, ir_rate

        return {
            "incidence_matrix": np.array(
                [[-1, 0], [1, -1], [0, 1]], np.float32
            ),
            "initial_state": np.array([[99, 1, 0]], np.float32),
            "num_steps": 199,
            "transition_rate_fn": rate_fn,
        }

    return fn


@pytest.fixture
def cont_time_homogeneous_sir_example():
    """An continuous time event list for an individual-level model"""

    return {
        "true_params": {"beta": 0.2, "gamma": 0.14},
        "example_events": EventList(
            time=np.array(
                [
                    1.0549483,
                    2.1438026,
                    4.955404,
                    5.0629563,
                    6.0129037,
                    9.736773,
                    10.073549,
                    10.724768,
                    10.983985,
                    11.556592,
                    11.88267,
                    12.320808,
                    12.480198,
                    12.72492,
                    12.766979,
                    13.567913,
                    15.699766,
                    16.780127,
                    16.812475,
                    17.256,
                    17.58674,
                    17.841612,
                    19.268337,
                    19.462679,
                    19.689648,
                    20.926064,
                    21.04814,
                    21.729326,
                    22.731691,
                    22.77068,
                    23.396738,
                    23.542427,
                    23.600094,
                    24.240898,
                    24.755678,
                    26.01209,
                    26.47591,
                    26.834217,
                    27.319405,
                    27.340483,
                    27.59122,
                    27.797024,
                    27.87457,
                    31.833166,
                    32.41091,
                    32.553165,
                    32.641747,
                    33.79145,
                    33.98341,
                    34.376286,
                    35.365017,
                    35.571873,
                    36.755424,
                    37.17231,
                    37.212296,
                    37.94769,
                    38.684868,
                    38.970898,
                    39.029892,
                    39.71459,
                    39.87689,
                    40.091244,
                    40.65399,
                    40.857,
                    42.495136,
                    43.802948,
                    45.751385,
                    49.511192,
                    53.19604,
                    53.32087,
                    53.33517,
                    53.872467,
                    56.630093,
                    57.11412,
                    57.63348,
                    57.65177,
                    59.498993,
                    np.inf,
                    np.inf,
                    np.inf,
                ],
                dtype=np.float32,
            ),
            transition=np.array(
                [
                    0,
                    1,
                    0,
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    1,
                    1,
                    1,
                    0,
                    0,
                    0,
                    0,
                    1,
                    0,
                    0,
                    0,
                    1,
                    1,
                    0,
                    0,
                    1,
                    0,
                    0,
                    0,
                    1,
                    1,
                    1,
                    1,
                    0,
                    1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    0,
                    0,
                    0,
                    0,
                    1,
                    1,
                    0,
                    0,
                    0,
                    1,
                    0,
                    0,
                    0,
                    1,
                    1,
                    1,
                    1,
                    1,
                    0,
                    1,
                    1,
                    1,
                    1,
                    0,
                    0,
                    1,
                    0,
                    1,
                    1,
                    1,
                    0,
                    1,
                    1,
                    2,
                    2,
                    2,
                ],
                dtype=np.int32,
            ),
            individual=np.array(
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                dtype=np.int32,
            ),
        ),
    }


@pytest.fixture()
def two_unit_sir_params():
    """Function to generate arguments for a two-unit SIR model
    given values for transition parameters."""

    def fn(beta=1.2, phi=2.0, gamma=0.14):
        initial_state = tf.constant([[99, 1, 0], [100, 0, 0]], tf.float32)
        incidence_matrix = tf.constant([[-1, 0], [1, -1], [0, 1]], tf.float32)
        contact = tf.constant([[0, 0.5], [0.5, 0]], tf.float32)

        def rate_fn(t, state):
            popsize = tf.reduce_sum(state, axis=-1)

            si_rate = (
                beta
                * (
                    state[:, 1]
                    + phi * tf.linalg.matvec(contact, state[:, 1] / popsize)
                )
                / tf.reduce_sum(state, axis=-1)
            )
            ir_rate = tf.constant(
                [gamma, gamma], tf.float32
            )  # tf.broadcast_to([0.14], si_rate.shape)
            return si_rate, ir_rate

        return {
            "incidence_matrix": incidence_matrix,
            "initial_state": initial_state,
            "transition_rate_fn": rate_fn,
            "num_steps": 50,
        }

    return fn


@pytest.fixture(scope="module")
def discrete_two_unit_sir_example():
    """Two-unit SIR epidemic for 50 timepoints"""
    return np.array(
        [
            [[1.0, 0.0], [0.0, 0.0]],
            [[1.0, 0.0], [0.0, 0.0]],
            [[4.0, 0.0], [0.0, 0.0]],
            [[7.0, 1.0], [0.0, 0.0]],
            [[17.0, 0.0], [1.0, 0.0]],
            [[16.0, 5.0], [2.0, 0.0]],
            [[24.0, 4.0], [3.0, 0.0]],
            [[17.0, 6.0], [4.0, 0.0]],
            [[9.0, 9.0], [13.0, 1.0]],
            [[3.0, 12.0], [22.0, 3.0]],
            [[0.0, 8.0], [20.0, 5.0]],
            [[0.0, 10.0], [14.0, 7.0]],
            [[0.0, 6.0], [12.0, 13.0]],
            [[0.0, 4.0], [7.0, 6.0]],
            [[0.0, 4.0], [1.0, 12.0]],
            [[0.0, 8.0], [0.0, 8.0]],
            [[0.0, 1.0], [0.0, 4.0]],
            [[0.0, 1.0], [1.0, 5.0]],
            [[0.0, 1.0], [0.0, 4.0]],
            [[0.0, 2.0], [0.0, 5.0]],
            [[0.0, 5.0], [0.0, 2.0]],
            [[0.0, 1.0], [0.0, 3.0]],
            [[0.0, 2.0], [0.0, 7.0]],
            [[0.0, 3.0], [0.0, 2.0]],
            [[0.0, 0.0], [0.0, 1.0]],
            [[0.0, 1.0], [0.0, 2.0]],
            [[0.0, 0.0], [0.0, 2.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 1.0]],
            [[0.0, 0.0], [0.0, 1.0]],
            [[0.0, 1.0], [0.0, 1.0]],
            [[0.0, 0.0], [0.0, 2.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 1.0], [0.0, 0.0]],
            [[0.0, 1.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 3.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 1.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 1.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 1.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 0.0]],
        ],
        dtype=np.float32,
    )
