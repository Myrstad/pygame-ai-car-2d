class Layer:
  """ Base layer class """
  def __init__(self):
    self.input = None
    self.output = None

  def forward(self, input: list[float]) -> list[float]:
    """forward computes the output Y of a layer for a given input X

    Raises:
        NotImplementedError: this is a super class and this behavior should be implemented
    """
    raise NotImplementedError
  
  def get_params(self) -> dict:
    """get_params of the layer

    Raises:
        NotImplementedError: this is a super class and this behavior should be implemented

    Returns:
        dict: params of the layer, includes everything
    """
    raise NotImplementedError

  def set_params(self, params:dict) -> None:
    """set_params from loaded data

    Raises:
        NotImplementedError: this is a super class and this behavior should be implemented
    """
    raise NotImplementedError
