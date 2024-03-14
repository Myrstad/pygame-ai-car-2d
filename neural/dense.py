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