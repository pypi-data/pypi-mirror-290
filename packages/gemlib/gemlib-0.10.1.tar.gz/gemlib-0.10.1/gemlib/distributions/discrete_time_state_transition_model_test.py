# Dependency imports
import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import test_util

from gemlib.distributions.discrete_markov import compute_state
from gemlib.distributions.discrete_time_state_transition_model import (
    DiscreteTimeStateTransitionModel,
)


@test_util.test_all_tf_execution_regimes
class TestDiscreteTimeStateTransitionModel(test_util.TestCase):
    @pytest.fixture(autouse=True)
    def _request_two_unit_sir_params(self, two_unit_sir_params):
        print("two_unit_sir_params:", two_unit_sir_params)
        self._two_unit_sir_params = two_unit_sir_params

    @pytest.fixture(autouse=True)
    def _request_discrete_two_unit_sir_example(
        self, discrete_two_unit_sir_example
    ):
        self._discrete_two_unit_sir_example = discrete_two_unit_sir_example

    def setUp(self):
        self.dtype = tf.float32
        self.incidence_matrix = [[-1, 0], [1, -1], [0, 1]]
        self.initial_state_A = [[99, 1, 0]]
        self.initial_state_B = [[8000, 2000, 0]]
        self.beta = 0.28
        self.gamma = 0.14
        self.nsim = 50

    def init_model(
        self,
        beta,
        gamma,
        incidence_matrix,
        initial_state,
        initial_step=0.0,
        time_delta=1.0,
        num_steps=100,
    ):
        def txrates(t, state):
            si = beta * state[:, 1] / tf.reduce_sum(state)
            ir = tf.broadcast_to([gamma], si.shape)
            return si, ir

        return DiscreteTimeStateTransitionModel(
            transition_rate_fn=txrates,
            incidence_matrix=incidence_matrix,
            initial_state=initial_state,
            initial_step=initial_step,
            time_delta=time_delta,
            num_steps=num_steps,
        )

    def test_float32(self):
        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_A, self.dtype)
        beta = tf.constant(self.beta, self.dtype)
        gamma = tf.constant(self.gamma, self.dtype)

        sir = self.init_model(
            beta, gamma, incidence_matrix, initial_state, num_steps=5
        )

        eventlist = sir.sample(seed=[0, 0])
        eventlist_ = self.evaluate(eventlist)
        self.assertDTypeEqual(eventlist_, np.float32)

        print("eventlist: ", eventlist)
        lp = sir.log_prob(eventlist)
        lp_ = self.evaluate(lp)
        self.assertDTypeEqual(lp_, np.float32)

    def test_float64(self):
        dtype = tf.float64
        incidence_matrix = tf.constant(self.incidence_matrix, dtype)
        initial_state = tf.constant(self.initial_state_A, dtype)
        beta = tf.constant(self.beta, dtype)
        gamma = tf.constant(self.gamma, dtype)

        sir = self.init_model(
            beta,
            gamma,
            incidence_matrix,
            initial_state,
            num_steps=5,
        )

        eventlist = sir.sample()
        eventlist_ = self.evaluate(eventlist)
        self.assertDTypeEqual(eventlist_, np.float64)
        lp = sir.log_prob(eventlist)
        lp_ = self.evaluate(lp)
        self.assertDTypeEqual(lp_, np.float64)

    def test_log_prob_and_grads(self):
        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_A, self.dtype)

        sir = self.init_model(
            self.beta,
            self.gamma,
            incidence_matrix,
            initial_state,
            initial_step=1.5,
            time_delta=0.5,
            num_steps=100,
        )

        eventlist = sir.sample()

        lp_and_grads = tfp.math.value_and_gradient(sir.log_prob, eventlist)
        lp_and_grads_ = self.evaluate(lp_and_grads)

        self.assertDTypeEqual(lp_and_grads_[0], self.dtype)

    def test_non_integer_time_steps(self):
        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_A, self.dtype)

        sir = self.init_model(
            self.beta,
            self.gamma,
            incidence_matrix,
            initial_state,
            initial_step=1.5,
            time_delta=0.5,
            num_steps=100,
        )

        eventlist = sir.sample()
        self.assertShapeEqual(np.ndarray(shape=(100, 1, 2)), eventlist)

        lp = sir.log_prob(eventlist)
        self.assertShapeEqual(np.ndarray(shape=()), lp)

    def test_log_prob(self):
        model = DiscreteTimeStateTransitionModel(**self._two_unit_sir_params())

        lp = self.evaluate(model.log_prob(self._discrete_two_unit_sir_example))

        actual_mean = -156.89182
        self.assertAllClose(lp, actual_mean)

    def test_model_constraints(self):
        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_A, self.dtype)
        time_delta = 1.0
        num_steps = 100

        sir = self.init_model(
            self.beta,
            self.gamma,
            incidence_matrix,
            initial_state,
            time_delta=time_delta,
            num_steps=num_steps,
        )

        eventlist = sir.sample(sample_shape=self.nsim, seed=[0, 0])
        ts = compute_state(initial_state, eventlist, incidence_matrix)

        # Crude check that some simulations have nontrivial dynamics
        # i.e. some units arrived in recovered compartments for some simulations
        sum_at_tmax = tf.reduce_sum(ts[:, num_steps - 1, :, 2])
        test_sum_at_tmax = (
            tf.cast(self.nsim * num_steps, self.dtype) / 4
        )  # factor 4 is a choice
        self.assertGreater(
            self.evaluate(sum_at_tmax), self.evaluate(test_sum_at_tmax)
        )

        # Check N is conserved at each time point
        # Note dS/dt + dI/dt + dR/dt = 0 then integrating over dt leads to
        # N = S + I + R
        sums_at_t = tf.vectorized_map(
            fn=lambda t: tf.reduce_sum(ts[:, t, :, :]),
            elems=tf.range(num_steps),
        )
        expected_sums = tf.broadcast_to(
            tf.cast(self.nsim * num_steps, self.dtype), [num_steps]
        )
        self.assertAllClose(sums_at_t, expected_sums, rtol=1e-06, atol=1e-06)

        # Check dS/dt + dI/dt + dR/dt = 0 at each time point
        finite_diffs = tf.reduce_sum(
            (ts[:, 1:, ...] - ts[:, :-1, ...]) / sir.time_delta
        )
        expected_diffs = tf.zeros_like(finite_diffs, self.dtype)
        self.assertAllClose(
            finite_diffs, expected_diffs, rtol=1e-06, atol=1e-06
        )

    def test_model_dynamics(self):
        """Check simulation adheres to the SIR system of ODEs.

        This check is performed without being in the thermodynamic limit
        (N->inf, t->inf).

        Let dS/dt=-bIS/N, dI/dt=bIS/N-gI and dR/dt=gI.
        Dividing first equation by third gives dS/dR=-b/g.S/N.
        Separating variables and integrating wrt dR yields
        int(1/S, dS)=-b/g.1/N.int(1, dR).
        Let the integrals have limits S(0), S(t), R(0), R(t).
        The solution to this integral is the transcendental equation
        S(t)=S(0)exp(-b/g.(R(t)-R(0))/N).  Due the stochastic nature of the
        chain binomial algorithm naively checking the simulated right
        hand side of this solution equals (with a given tolerence) the simulated
        left hand side is fraught with difficulty.  However rearranging the
        solution in terms of the time invariant factor
        b/g=-N.ln(S(t)/S(0))/(R(t)-R(0)) makes it possible to check the
        simulated dynamics adhere to the dynamics given by the SIR system of
        ODEs (except when R(t)=R0).

        """

        incidence_matrix = tf.constant(self.incidence_matrix, self.dtype)
        initial_state = tf.constant(self.initial_state_B, self.dtype) * 10
        num_steps = 200
        buffer = 20  # number if initial steps to be omitted

        sir = self.init_model(
            self.beta,
            self.gamma,
            incidence_matrix,
            initial_state,
            time_delta=0.25,
            num_steps=num_steps,
        )

        eventlist = sir.sample(sample_shape=self.nsim, seed=[0, 0])
        ts = sir.compute_state(eventlist)

        S0 = initial_state[0, 0]
        R0 = initial_state[0, 2]
        St = ts[..., 0, 0]
        Rt = ts[..., 0, 2]
        N = tf.reduce_sum(initial_state)
        r0_sim = -N * tf.math.log(St / S0) / (Rt - R0)  # r0=beta/gamma

        # Crude check that some simulations have nontrivial dynamics
        sum_at_tmax = tf.reduce_sum(ts[:, num_steps - 1, :, 2])
        test_sum_at_tmax = (
            tf.cast(self.nsim * num_steps, self.dtype) / 4
        )  # factor 4 is a choice
        self.assertGreater(
            self.evaluate(sum_at_tmax), self.evaluate(test_sum_at_tmax)
        )

        # First time step must be omitted as it will be undefined due to
        #   division by zero n.b. R(t=0)=R0
        # Soft test - summarise the mean of each simulation
        mean_r0_sim = tf.reduce_mean(r0_sim[:, buffer:num_steps], axis=1)
        r0_actual = tf.broadcast_to(self.beta / self.gamma, [self.nsim])
        self.assertAllClose(
            mean_r0_sim, r0_actual, rtol=1e-06, atol=0.11
        )  # atol scales inversely with the size of N

        # Hard test - check all times apart from a few initial steps when R(t)
        # may equal R0
        r0_all_actual = tf.broadcast_to(
            self.beta / self.gamma, [self.nsim, num_steps - buffer]
        )
        self.assertAllClose(
            r0_sim[:, buffer:num_steps], r0_all_actual, rtol=1e-06, atol=0.14
        )


@test_util.test_all_tf_execution_regimes
class TestDiscreteTimeStateTransitionModelLogProbMaxima(test_util.TestCase):
    def init_model(self, params, incidence_matrix, initial_state):
        beta, gamma = tf.unstack(params)

        def txrates(t, state):
            si = beta * state[:, 1] / tf.reduce_sum(state, axis=-1)
            ir = tf.broadcast_to([gamma], si.shape)
            return si, ir

        return DiscreteTimeStateTransitionModel(
            transition_rate_fn=txrates,
            incidence_matrix=incidence_matrix,
            initial_state=initial_state,
            initial_step=0.0,
            time_delta=1.0,
            num_steps=100,
        )

    def test_log_prob_mle(self):
        """Test maximum likelihood estimation"""

        dtype = np.float32
        incidence_matrix = tf.constant([[-1, 0], [1, -1], [0, 1]], dtype)
        initial_state = tf.constant([[980, 20, 0]], dtype)
        pars = tf.constant([0.2, 0.14], dtype)

        # Simulate a dataset
        sir_orig = self.init_model(pars, incidence_matrix, initial_state)
        events = self.evaluate(sir_orig.sample(seed=(0, 0)))

        def logp(pars):
            lp = self.init_model(
                tf.math.exp(pars), incidence_matrix, initial_state
            ).log_prob(events)
            return -lp

        optim_results = tfp.optimizer.nelder_mead_minimize(
            logp,
            initial_vertex=tf.zeros_like(pars),
            func_tolerance=1e-4,
        )
        print(self.evaluate(optim_results))

        self.assertAllTrue(optim_results.converged)
        self.assertAllClose(
            tf.math.exp(optim_results.position), pars, rtol=0.1, atol=0.1
        )


if __name__ == "__main__":
    tf.test.main()
