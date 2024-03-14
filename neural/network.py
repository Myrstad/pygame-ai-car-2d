class Network:
  def __init__(self):
    self.layers = []
  
  def add(self, layer):
    self.layers.append(layer)

  def forward(self, input_data):
    """Propagate input through the network"""
    output = input_data
    for layer in self.layers:
      output = layer.forward(output)
    return output
  