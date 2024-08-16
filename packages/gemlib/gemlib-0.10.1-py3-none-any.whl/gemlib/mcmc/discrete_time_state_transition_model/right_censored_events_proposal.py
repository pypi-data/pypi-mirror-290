import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.distributions import Categorical2, UniformInteger

tfd = tfp.distributions


def add_occult_proposal(
    events,
    topology,
    initial_state,
    n_max,
    t_range=None,
    dtype=tf.int32,
    name=None,
):
    if t_range is None:
        t_range = [0, events.shape[-2]]

    def m():
        """Select a metapopulation"""
        with tf.name_scope("m"):
            return UniformInteger(
                low=[0],
                high=[events.shape[0]],
                dtype=dtype,
                float_dtype=events.dtype,
            )

    def t():
        """Select a timepoint"""
        with tf.name_scope("t"):
            return UniformInteger(
                low=[t_range[0]],
                high=[t_range[1]],
                dtype=dtype,
                float_dtype=events.dtype,
            )

    def x_star(m, t):
        """Draw num to add bounded by counting process contraint"""
        if topology.prev is not None:
            mask = (  # Mask out times prior to t
                tf.cast(tf.range(events.shape[-2]) < t[0], events.dtype)
                * events.dtype.max
            )
            m_events = tf.gather(events, m, axis=-3)
            m_inits = tf.gather(initial_state, m, axis=-2)
            diff = m_events[..., topology.prev] - m_events[..., topology.target]
            diff = tf.gather(m_inits, topology.target, axis=-1) + tf.cumsum(
                diff, axis=-1
            )
            diff = diff + mask
            bound = tf.cast(tf.reduce_min(diff, axis=-1), dtype=tf.int32)
            # bound = tf.maximum(0, bound)
            bound = tf.minimum(n_max, bound)
        else:
            bound = tf.broadcast_to(n_max, m.shape)

        return UniformInteger(
            low=1, high=bound + 1, dtype=dtype, float_dtype=events.dtype
        )

    return tfd.JointDistributionNamed(
        {"m": m, "t": t, "x_star": x_star}, name=name
    )


def del_occult_proposal(
    events,
    topology,
    initial_state,
    n_max,
    t_range=None,
    dtype=tf.int32,
    name=None,
):
    if t_range is None:
        t_range = [0, events.shape[-2]]

    def m():
        """Select a metapopulation"""
        with tf.name_scope("m"):
            hot_meta = (
                tf.math.count_nonzero(
                    events[..., slice(*t_range), topology.target],
                    axis=1,
                    keepdims=True,
                )
                > 0
            )
            hot_meta = tf.cast(tf.transpose(hot_meta), dtype=events.dtype)
            logits = tf.math.log(hot_meta)
            X = Categorical2(
                logits=tf.cast(logits, tf.float32), dtype=dtype, name="m"
            )
            return X

    def t(m):
        """Draw timepoint"""
        with tf.name_scope("t"):
            metapops = tf.gather(events, m)
            hot_times = (
                (metapops[..., topology.target] > 0)
                & (t_range[0] <= tf.range(events.shape[-2]))
                & (tf.range(events.shape[-2]) < t_range[1])
            )
            hot_times = tf.cast(hot_times, dtype=events.dtype)
            logits = tf.math.log(hot_times)
            return Categorical2(
                logits=tf.cast(logits, tf.float32), dtype=dtype, name="t"
            )

    def x_star(m, t):
        """Draw num to delete"""
        with tf.name_scope("x_star"):
            if topology.next is not None:
                mask = (  # Mask out times prior to t
                    tf.cast(tf.range(events.shape[-2]) < t[0], events.dtype)
                    * events.dtype.max
                )
                m_events = tf.gather(events, m, axis=-3)
                m_inits = tf.gather(initial_state, m, axis=-2)
                # calc offset[target] + N_{target}(t) - N_{next} bound
                diff = (
                    m_events[..., topology.target]
                    - m_events[..., topology.next]
                )
                diff = tf.gather(m_inits, topology.next, axis=-1) + tf.cumsum(
                    diff, axis=-1
                )
                diff = diff + mask
                bound = tf.cast(tf.reduce_min(diff, axis=-1), dtype=tf.int32)
                # bound = tf.maximum(0, bound)
                bound = tf.minimum(n_max, bound)
            else:
                bound = tf.broadcast_to(n_max, m.shape)

            return UniformInteger(
                low=1,
                high=bound + 1,
                dtype=dtype,
                float_dtype=events.dtype,
                name="x_star",
            )

    return tfd.JointDistributionNamed(
        {"m": m, "t": t, "x_star": x_star}, name=name
    )
