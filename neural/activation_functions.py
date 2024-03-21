import numpy as np

def sigmoid(x: list[float]|np.ndarray) -> np.ndarray:
  return 1 / (1 + np.exp(-x))

def ReLU(x: list[float]|np.ndarray) -> np.ndarray:
  return np.maximum(0, x)