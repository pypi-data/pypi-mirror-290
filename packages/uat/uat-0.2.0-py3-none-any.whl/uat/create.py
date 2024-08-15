from jax.random import split, normal


def create(key, dims):
    input_dim, output_dim, neurons = dims
    shapes = [(input_dim, neurons), (1, neurons), (neurons, output_dim)]
    return tuple(normal(key, shape) for key, shape in zip(split(key, 3), shapes))
