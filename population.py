from copy import deepcopy
from environment import Environment
from car import Car
from neural import Network, Dense, ActivationLayer, sigmoid, ReLU
import numpy as np

class Population:
  def __init__(self, name, *, size=100, learning_rate=0.1, trained_model=None) -> None:
    self.name = name
    self.size = size
    self.learning_rate = learning_rate
    self.selection_ratio = 0.25
    self.generation = 0
    self.elites = 1

    self.environment: Environment = Environment("models/simple.json")
    self.cars: list[Car] = [Car(self.environment, True) for _ in range(size)] #all cars have a fitness attribute
    self.population: list[Network] = self.init_population()
    if trained_model:
      self.load_network(trained_model)
  
  def init_population(self):
    population = [Network() for _ in range(self.size)]
    for network in population:
      network.add(Dense(len(self.cars[0].get_neural_network_input()),8))
      network.add(ActivationLayer(ReLU))
      network.add(Dense(8,8))
      network.add(ActivationLayer(ReLU))
      network.add(Dense(8,4))
      network.add(ActivationLayer(sigmoid))

    return population

  def re_populate_with_mutation(self):
    population_size = len(self.population)
    times = self.size // population_size
    new_population = []
    for pop in self.population:
      for i in range(times):
        if i == 0:
          new_population.append(pop)
        else:
          net = deepcopy(pop)
          net.mutate(self.learning_rate)
          new_population.append(net)
    
    return new_population

  def get_fitnesses(self) -> list[int]:
    return [car.fitness for car in self.cars]

  def selection(self) -> list[Network]:
    """Perform selection of parents based on their fitness"""
    number_of_selected = int(self.selection_ratio * len(self.population))
    sorted_indices = np.argsort(self.get_fitnesses())[::-1]
    selected_indices = sorted_indices[:number_of_selected]
    selected_individuals = [self.population[i] for i in selected_indices]
    return selected_individuals

  def evolve(self):
    self.generation += 1
    
    self.population = self.selection()
    self.population = self.re_populate_with_mutation()
    self.save_network(self.population[0]) #hopefully
    # self.environment = Environment()
    self.cars = [Car(self.environment, True) for _ in range(len(self.population))]
  
  def save_network(self, network:Network):
    network.save(f'models/{self.name}.pkl')
  
  def load_network(self, filename):
    self.population.pop()
    net = Network()
    net.load(filename)
    self.population.insert(0, net)


if __name__ == '__main__':
  p = Population("test", size=12)
  p.evolve()
  # copy = Population("test", size=4, learning_rate=0, trained_model="models/test.pkl")
  # copy.evolve()
