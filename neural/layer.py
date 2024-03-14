class Layer:
  """ Base class """
  def __init__(self):
    self.input = None
    self.output = None

  def forward(self, input):
    """ computes the output Y of a layer for a given input X """
    raise NotImplementedError