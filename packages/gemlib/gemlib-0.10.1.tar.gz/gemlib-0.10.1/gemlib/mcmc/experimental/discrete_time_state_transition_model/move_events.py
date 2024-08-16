"""Move partially-censored events in DiscreteTimeStateTransitionModel"""

from typing import NamedTuple

import tensorflow_probability as tfp

from gemlib.mcmc.discrete_time_state_transition_model import (
    UncalibratedEventTimesUpdate,
)

from ..sampling_algorithm import ChainState, SamplingAlgorithm


class MoveEventsState(NamedTuple):
    num_units: int
    delta_max: int
    count_max: int


class MoveEventsInfo(NamedTuple):
    is_accepted: bool
    initial_conditions: float


def move_events(
    incidence_matrix, target_transition_id, num_units, delta_max, count_max
):
    def _build_kernel(target_log_prob_fn, initial_conditions):
        return tfp.mcmc.MetropolisHastings(
            inner_kernel=UncalibratedEventTimesUpdate(
                target_log_prob_fn,
                incidence_matrix=incidence_matrix,
                initial_conditions=initial_conditions,
                target_transition_id=target_transition_id,
                num_units=num_units,
                delta_max=delta_max,
                count_max=count_max,
                name="move_events",
            )
        )

    def init_fn(target_log_prob_fn, target_state, initial_conditions):
        kernel = _build_kernel(target_log_prob_fn, initial_conditions)
        results = kernel.bootstrap_results(target_state)
        chain_state = ChainState(
            position=target_state,
            log_density=results.accepted_results.target_log_prob,
        )
        kernel_state = MoveEventsState(num_units, delta_max, count_max)

        return chain_state, kernel_state

    def step_fn(
        target_log_prob_fn, target_and_kernel_state, seed, initial_conditions
    ):
        kernel = _build_kernel(target_log_prob_fn, initial_conditions)

        target_chain_state, kernel_state = target_and_kernel_state

        new_target_position, results = kernel.one_step(
            target_chain_state.position,
            kernel.bootstrap_results(target_chain_state.position),
            seed=seed,
        )

        new_chain_and_kernel_state = (
            ChainState(
                position=new_target_position,
                log_density=results.accepted_results.target_log_prob,
            ),
            kernel_state,
        )

        return new_chain_and_kernel_state, MoveEventsInfo(
            results.is_accepted, initial_conditions
        )

    return SamplingAlgorithm(init_fn, step_fn)
