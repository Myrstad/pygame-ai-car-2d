from copy import deepcopy
from environment import Environment
from car import Car
from neural import Network, Dense, ActivationLayer, sigmoid, ReLU
import numpy as np
import pygame as pg
from settings import ENVIRONMENT_PATH, BLACK

class Population:
  """Population class for storing neural networks with cars they control.
  
  Used for creating better and better neural networks for the circuits.
  Keeps track of generation and the best networks for each generation to
  a save file. That can later be loaded. 
  """
  def __init__(self, name: str, *, size: int = 100, learning_rate: float = 0.1, trained_model: str = None) -> None:
    """__init__ Population

    Args:
        name (str): name of population and used for saving model
        size (int, optional): population size. Defaults to 100.
        learning_rate (float, optional): max amount of possible change per gen. Defaults to 0.1.
        trained_model (str, optional): Loading in previous network. Defaults to None.
    """
    self.name = name
    self.size = size
    self.learning_rate = learning_rate
    self.selection_ratio = 0.25
    self.generation = 0
    self.elites = 1
    self.prev_best = None

    self.environment: Environment = Environment(ENVIRONMENT_PATH)
    self.cars: list[Car] = [Car(self.environment, True) for _ in range(size)] #all cars have a fitness attribute
    self.population: list[Network] = self.init_population()
    if trained_model:
      self.load_network(trained_model)
  
  def init_population(self) -> list[Network]:
    """init_population to a standard network

    Returns:
        list[Network]: starting population
    """
    population = [Network() for _ in range(self.size)]
    for network in population:
      network.add(Dense(len(self.cars[0].get_neural_network_input()),8))
      network.add(ActivationLayer(ReLU))
      network.add(Dense(8,8))
      network.add(ActivationLayer(ReLU))
      network.add(Dense(8,4))
      network.add(ActivationLayer(sigmoid))

    return population

  def re_populate_with_mutation(self) -> list[Network]:
    """re_populate_with_mutation

    Returns:
        list[Network]: next generation population
    """
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
    """get_fitnesses

    Returns:
        list[int]: all the fitnesses connected to the cars
    """
    return [car.fitness for car in self.cars]

  def selection(self) -> list[Network]:
    """selection of "parents" based on their fitness

    Returns:
        list[Network]: The best performing networks
    """
    number_of_selected = int(self.selection_ratio * len(self.population))
    sorted_indices = np.argsort(self.get_fitnesses())[::-1]
    selected_indices = sorted_indices[:number_of_selected]
    selected_individuals = [self.population[i] for i in selected_indices]
    return selected_individuals

  def evolve(self) -> None:
    """evolve to get the next population, saves if learning rate != 0"""
    self.generation += 1
    self.prev_best = max([int(car.fitness) for car in self.cars])
    
    if self.learning_rate == 0:
      self.cars = [Car(self.environment, True) for _ in range(len(self.population))]
      return
    self.population = self.selection()
    self.population = self.re_populate_with_mutation()
    self.save_network(self.population[0]) #hopefully
    # self.environment = Environment()
    self.cars = [Car(self.environment, True) for _ in range(len(self.population))]
  
  def save_network(self, network:Network) -> None:
    """save_network

    Args:
        network (Network): should be the best performing network
    """
    network.save(f'models/{self.name}.pkl')
  
  def load_network(self, filename: str) -> None:
    """load_network and use it as a baseline for the population

    Args:
        filename (str): filename with path to saved network
    """
    self.population.clear()
    net = Network()
    net.load(filename)
    self.population.append(net)
    self.population = self.re_populate_with_mutation()
  
  def draw_debug_info(self, screen: pg.Surface) -> None:
    font: pg.font.Font = pg.font.SysFont(None, 20)
    current_best: pg.Surface = font.render(f'Current best fitness: {max([int(car.fitness) for car in self.cars])}', True, BLACK)
    prev_best: pg.Surface = font.render(f'Previous best fitness: {self.prev_best}', True, BLACK)
    current_generation: pg.Surface = font.render(f'Generation: {self.generation}', True, BLACK)
    #draw to top lef
    screen.blit(current_generation, (32, 32))
    screen.blit(prev_best, (32, 32+20))
    screen.blit(current_best, (32, 32+20*2))

if __name__ == '__main__':
  p = Population("test", size=12)
  p.evolve()
  # copy = Population("test", size=4, learning_rate=0, trained_model="models/test.pkl")
  # copy.evolve()
