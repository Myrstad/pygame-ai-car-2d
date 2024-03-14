from .layer import Layer

class ActivationLayer(Layer):
  def __init__(self, activation):
    self.activation = activation

  def forward(self, input_data):
    """returns the activated input"""
    self.input = input_data
    self.output = self.activation(self.input)
    return self.output