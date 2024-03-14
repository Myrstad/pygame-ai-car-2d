from .activation_functions import *
from .dense import Dense
from .activation_layer import ActivationLayer
from .network import Network

if __name__ == '__main__':
  """ Command to test this code `python3 -m neural.__init__` from the main folder """
  net = Network()
  net.add(Dense(5, 7))
  net.add(ActivationLayer(ReLU))
  net.add(Dense(7, 2))
  net.add(ActivationLayer(ReLU))
  # print(net.forward([1,2,3,4,5]), type(net.forward([1,2,3,4,5])))
  # print(net.layers[0].input)
  # print(net.__dict__)
  print(net.layers[-2].__dict__)
  for layer in net.layers:
    # print(layer.__dict__)
    pass
  print()
  net.save("models/test.pkl")

  test = Network()
  test.load("models/test.pkl")
  # print(test.__dict__)
  print(test.layers[-2].__dict__)