# uat

Universal Approximation Theorem in JAX

```
pip install uat
```

## Universal Approximation Theorem

The Universal Approximation Theorem states that a feedforward neural network with a single hidden layer containing a finite number of neurons can approximate any continuous function on compact subsets of $\mathbb{R}^n$, given appropriate activation functions.

### General Formula

The general formula for a neural network with one hidden layer can be expressed as:

$$f(x) = \sum_{i=1}^{N} c_i \sigma(a_i \cdot x + b_i)$$

where:
- $x$ is the input vector.
- $N$ is the number of neurons in the hidden layer.
- $a_i$ and $b_i$ are the weights and biases of the neurons in the hidden layer.
- $c_i$ are the weights of the output layer.
- $\sigma$ is the activation function (e.g., sigmoid, tanh).

## Activation Function

The Universal Approximation Theorem (UAT) hinges on the choice of activation function used in the neural network. Not all activation functions are suitable for ensuring that a neural network can approximate any continuous function on compact subsets of $\mathbb{R}^n$. Here are the key requirements and considerations for activation functions in the context of the UAT:

### Requirements

1. **Non-linearity**: The activation function must be non-linear. Linear activation functions (like the identity function) do not introduce the necessary complexity for the network to approximate non-linear functions.

2. **Boundedness**: The activation function should be bounded. This means that the output of the activation function should lie within a fixed range. For example, the sigmoid function outputs values in the range (0, 1).

3. **Continuity**: The activation function should be continuous. Discontinuous activation functions can lead to issues in training and may not satisfy the conditions of the UAT.

4. **Non-constant**: The activation function should not be a constant function. A constant activation function would not allow the network to learn any meaningful patterns from the input data.

### Common Activation Functions

Here are some commonly used activation functions that satisfy the requirements of the UAT:

- **Sigmoid**: $\sigma(x) = \frac{1}{1 + e^{-x}}$
  - Bounded between 0 and 1.
  - Non-linear and continuous.
  
- **Tanh**: $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$
  - Bounded between -1 and 1.
  - Non-linear and continuous.

## Creating a Model

To create a model, use the `create` function. This function initializes the parameters of the model.

```python
from jax.random import PRNGKey
from uat import create

key = PRNGKey(0)
input_dim = 2
neurons = 2
output_dim = 1
dims = (input_dim, neurons, output_dim)
params = create(key, dims)
```

## Applying the Model

To apply the model to an input, use the `apply` function. This function computes the output of the model given the input and the model parameters.

```python
from jax.numpy import array
from uat import apply

x = array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
output = apply(params, x)
```

## Explanation of the `apply` Function

The `apply` function computes the output of the model using the following formula:

```python
def apply(params, x):
    a, b, c = params
    return sigmoid(x @ a + b) @ c
```

Here's a step-by-step explanation of the formula:

1. **Parameter Unpacking**: The parameters `params` are unpacked into three components: `a`, `b`, and `c`.
   - `a` is a matrix of shape `(input_dim, neurons)`.
   - `b` is a bias vector of shape `(1, neurons)`.
   - `c` is a weight matrix of shape `(neurons, output_dim)`.

2. **Matrix Multiplication**: The input `x` (of shape `(n_samples, input_dim)`) is multiplied by the matrix `a` using the `@` operator. This results in a matrix of shape `(n_samples, neurons)`.

3. **Bias Addition**: The bias vector `b` is added to the result of the matrix multiplication. Broadcasting is used to add `b` to each row of the matrix, resulting in a matrix of shape `(n_samples, neurons)`.

4. **Sigmoid Activation**: The sigmoid function `sigmoid` is applied element-wise to the result of the bias addition. This introduces non-linearity into the model.

5. **Output Calculation**: The resulting matrix (of shape `(n_samples, neurons)`) is then multiplied by the weight matrix `c` using the `@` operator. This results in the final output matrix of shape `(n_samples, output_dim)`.

## Training the Model on XOR

To train the model on the XOR problem, you can use the following code. This code uses stochastic gradient descent (SGD) to optimize the model parameters.

```python
from optax import sgd, apply_updates
from jax.numpy import array, allclose, abs, mean
from jax.random import PRNGKey
from jax import grad, jit
from uat import create, apply

# Initialize parameters
key = PRNGKey(0)
input_dim = 2
neurons = 2
output_dim = 1
dims = (input_dim, neurons, output_dim)
params = create(key, dims)

# XOR input and output
x = array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = array([[0], [1], [1], [0]], dtype=float)

# Define optimizer
optimizer = sgd(learning_rate=0.1, momentum=0.9)
state = optimizer.init(params)

# Define loss function
def loss(params, x, y):
    y_hat = apply(params, x)
    return mean(abs(y - y_hat))

# Define training step
@jit
def fit(state, params, x, y):
    grads = grad(loss)(params, x, y)
    updates, state = optimizer.update(grads, state)
    params = apply_updates(params, updates)
    return state, params

# Train the model
for _ in range(1000):
    state, params = fit(state, params, x, y)

# Check the output
y_hat = apply(params, x)
assert allclose(y, y_hat, atol=0.1)
```

This code initializes the model parameters, defines the XOR input and output, sets up the optimizer, and trains the model for 1000 iterations. Finally, it checks if the model's output is close to the expected XOR output.

## Note on Optimizer Compatibility

Since the `create` function outputs a pytree, you can use any JAX-based optimizer library like `optax` to optimize the model parameters. This allows for flexibility in choosing different optimization algorithms and techniques to train your model effectively.

## Creating Complex Approximation Models

By using this simple library, you can create complex approximation models. The flexibility of the Universal Approximation Theorem allows you to model a wide range of continuous functions, making it a powerful tool for various applications in machine learning and data science.
