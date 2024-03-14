class Layer:
  """ Base class """
  def __init__(self):
    self.input = None
    self.output = None

  def forward(self, input):
    """ computes the output Y of a layer for a given input X """
    raise NotImplementedError
  
  def get_params(self):
    raise NotImplementedError

  def set_params(self, params):
    """Set parameters from loaded data"""
    raise NotImplementedError
