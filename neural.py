class Layer(object):
  """ Base class """
  def __init__(self) -> None:
    self.input = None
    self.output = None
  
  def forward(self, input):
    raise NotImplementedError

class Dense(Layer):
  pass

class ActivationLayer(Layer):
  pass

class ReLu(ActivationLayer):
  pass