from .activation_functions import ReLU, sigmoid
from .dense import Dense
from .activation_layer import ActivationLayer
from .network import Network

if __name__ == '__main__':
  net = Network()
  net.add(Dense(5, 7))
  net.add(ActivationLayer(ReLU))
  net.add(Dense(7, 2))
  net.add(ActivationLayer(ReLU))
  print(net.forward([1,2,3,4,5]), type(net.forward([1,2,3,4,5])))
  print(net.layers[0].input)
  print()