import pickle
import numpy as np
from .dense import Dense
from .activation_layer import ActivationLayer

class Network:
  def __init__(self):
    self.layers: list[Dense|ActivationLayer] = []
  
  def add(self, layer):
    self.layers.append(layer)

  def forward(self, input_data):
    """Propagate input through the network"""
    output = input_data
    for layer in self.layers:
      output = layer.forward(output)
    return output
  
  def mutate(self, mutation_rate:float):
    """Apply mutation to the weights of the network"""
    for layer in self.layers:
      if isinstance(layer, Dense):
        layer.mutate(mutation_rate)

  def save(self, filename):
    """Save network parameters to a file"""
    params = [{'type': type(layer).__name__, 'params': layer.get_params()} for layer in self.layers]
    with open(filename, 'wb') as f:
      pickle.dump(params, f)
  
  def load(self, filename):
    """Load network parameters from a file"""
    with open(filename, 'rb') as f:
      params = pickle.load(f, )
    self.layers = []
    for param in params:
      layer_type = param['type']
      if layer_type == 'Dense':
        layer = Dense(0, 0)  # Create a temporary layer to call set_params
      elif layer_type == 'ActivationLayer':
        layer = ActivationLayer(lambda x: x)  # Placeholder activation function
      layer.set_params(param['params'])
      self.add(layer)