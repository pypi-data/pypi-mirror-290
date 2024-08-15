from jax.nn import sigmoid


def apply(params, x):
    a, b, c = params
    return sigmoid(x @ a + b) @ c
