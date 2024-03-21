from .layer import Layer
from typing import Callable
from .activation_functions import *

class ActivationLayer(Layer):
  """ActivationLayer uses a function to change the output of the `Dense` (fully connected) layer"""
  def __init__(self, activation: Callable) -> None:
    """__init__ the activation layer

    Args:
        activation (Callable): numpy function for changing output of `Dense` layer
    """
    self.activation_name: str = activation.__name__
    self.activation: function = activation

  def forward(self, input_data: list[float]) -> list[float]:
    """forward propagates

    Returns:
        list[float]: returns the output of prev layer after activation function
    """
    self.input = input_data
    self.output = self.activation(self.input)
    return self.output
  
  def get_params(self) -> dict:
    """get_params is almost static, only the name of the function is needed

    Returns:
        dict[str, str]: activation functions name
    """
    return {'activation_name': self.activation_name}

  def set_params(self, params: dict) -> None:
    """set_params from loaded data

    Args:
        dict: uses the activation name to get the correct function
    """ 
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