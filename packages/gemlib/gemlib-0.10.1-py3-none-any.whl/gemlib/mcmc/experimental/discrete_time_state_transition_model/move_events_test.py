"""Test partially censored events move for DiscreteTimeStateTransitionModel"""

import pytest
import tensorflow as tf

from .move_events import move_events


@pytest.fixture
def random_events():
    """SEIR model with prescribed starting conditions"""
    events = tf.random.uniform(
        [10, 10, 3], minval=0, maxval=100, dtype=tf.float64, seed=0
    )
    return events


@pytest.fixture
def initial_state():
    popsize = tf.fill([10], tf.constant(100.0, tf.float64))
    initial_state = tf.stack(
        [
            popsize,
            tf.ones_like(popsize),
            tf.zeros_like(popsize),
            tf.zeros_like(popsize),
        ],
        axis=-1,
    )
    return initial_state


@pytest.fixture
def incidence_matrix():
    return tf.constant(
        [[-1, 0, 0], [1, -1, 0], [0, 1, -1], [0, 0, 1]], tf.float64
    )


def test_move_events(random_events, initial_state, incidence_matrix):
    def tlp(x):
        return tf.constant(0.0, dtype=tf.float64)

    kernel = move_events(
        incidence_matrix,
        target_transition_id=1,
        num_units=1,
        delta_max=5,
        count_max=10,
    )

    state = kernel.init(tlp, random_events, initial_state)
    seed = [0, 0]
    new_state, results = kernel.step(tlp, state, seed, initial_state)
