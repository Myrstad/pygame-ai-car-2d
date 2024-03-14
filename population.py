from copy import deepcopy

class Population:
  def __init__(self, size) -> None:
    self.cars = [None for _ in range(size)]
  
  def selection(self, amount):
    """Perform selection of parents based on their fitness"""
    self.cars.sort(key=lambda x: x, reverse=True)
    elite = self.cars.pop(0)

if __name__ == '__main__':
  p = Population(100)
  p.selection(10)