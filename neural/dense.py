import numpy as np
from .layer import Layer

class Dense(Layer):
  """inherit from base class Layer"""
  # input_size = number of input neurons
  # output_size = number of output neurons
  def __init__(self, input_size, output_size):
    self.weights = np.random.rand(input_size, output_size) - 0.5
    self.bias = np.random.rand(1, output_size) - 0.5

  def forward(self, input_data):
    """returns output for a given input"""
    self.input = input_data
    self.output = np.dot(self.input, self.weights) + self.bias
    return self.output
  
  def mutate(self, mutation_rate:float) -> None:
    """Apply mutation to the weights and biases"""
    print(self.weights)
    self.weights += np.random.rand(*self.weights.shape) * mutation_rate
    print(self.weights)
  
  def get_params(self):
    """Return parameters for saving"""
    return {'weights': self.weights, 'bias': self.bias}

  def set_params(self, params):
    """Set parameters from loaded data"""
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
