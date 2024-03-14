from .layer import Layer
from typing import Callable
from .activation_functions import *

class ActivationLayer(Layer):
  def __init__(self, activation:Callable):
    self.activation_name:str = activation.__name__
    self.activation: function = activation

  def forward(self, input_data):
    """returns the activated input"""
    self.input = input_data
    self.output = self.activation(self.input)
    return self.output
  
  def get_params(self):
    """Activation layers have no parameters"""
    return {'activation_name': self.activation_name}

  def set_params(self, params):
    """Set parameters from loaded data"""
    self.activation_name = params['activation_name']
    # Dynamically import the activation function based on its name
    self.activation = globals()[self.activation_name]

if __name__ == '__main__':
  from .activation_functions import sigmoid
  al = ActivationLayer(sigmoid)
  params = al.get_params()
  new = ActivationLayer(lambda x: x) # placeholder
  new.set_params(params)
  print(new.__dict__)