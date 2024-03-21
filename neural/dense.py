import numpy as np
from .layer import Layer

class Dense(Layer):
  """inherit from base `Layer` class"""
  def __init__(self, input_size: int, output_size: int) -> None:
    """__init__ the Dense class

    Args:
        input_size (int): amount of input neurons
        output_size (int): amount of output neurons
    """
    self.weights = np.random.rand(input_size, output_size) - 0.5
    self.bias = np.random.rand(1, output_size) - 0.5

  def forward(self, input_data: list[float]) -> list[float]:
    """returns output for a given input"""
    """forward propagate

    Returns:
        list[float]: returns the output of this layer
    """
    self.input = input_data
    self.output = np.dot(self.input, self.weights) + self.bias
    return self.output
  
  def mutate(self, mutation_rate:float) -> None:
    """mutate apply mutation to the weight and biases

    Args:
        mutation_rate (float): mutates all genomes with +- [-mut_rate, +mut_rate]
    """
    self.weights += np.random.uniform(-mutation_rate, mutation_rate, size=self.weights.shape)
    self.bias += np.random.uniform(-mutation_rate, mutation_rate, size=self.bias.shape)
  
  def get_params(self):
    """get_params Return parameters for saving layer"""
    return {'weights': self.weights, 'bias': self.bias}

  def set_params(self, params):
    """set_params from loaded data"""
    self.weights = params['weights']
    self.bias = params['bias']

if __name__ == '__main__':
  from .activation_functions import sigmoid
  d = Dense(1,1)
  # print(d.__dict__)
  params = d.get_params()
  n = Dense(0,0)
  n.set_params(params)
  # print(n.__dict__)
  d.mutate(100)
