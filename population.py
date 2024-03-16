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
    self.generation = 0
    self.elites = 1

    self.environment: Environment = Environment()
    self.cars: list[Car] = [Car(self.environment, 110, 400, True) for _ in range(size)] #all cars have a fitness attribute
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

  def selection(self) -> list[Network]:
    """Perform selection of parents based on their fitness"""
    fitnesses = [car.fitness for car in self.cars]
    # fitnesses = [np.random.randint(-100, 1000) for car in self.cars]
    fitnesses = [x - min(fitnesses) + 1 for x in fitnesses] # in case of negative fitness
    total_fitness = sum(fitnesses)

    # Select top elites
    sorted_indexes = np.argsort(fitnesses)[::-1]  # Sort indexes in descending order of fitness
    elite_indexes = sorted_indexes[:self.elites]

    # Perform roulette wheel selection for the rest
    remaining_size = self.size - self.elites
    roulette_indexes = np.random.choice(self.size, size=remaining_size, p=np.array(fitnesses) / total_fitness)
    # Combine elite and roulette selections
    selected_indexes = []
    [selected_indexes.append(int(x)) for x in elite_indexes]
    [selected_indexes.append(int(x)) for x in roulette_indexes]
    return [deepcopy(self.population[i]) for i in selected_indexes]

  def evolve(self):
    self.generation += 1
    self.population = self.selection()
    self.save_network(self.population[0])
    # print(self.population[0])
    for i in range(self.elites, self.size):
      self.population[i].mutate(self.learning_rate)
    for car in self.cars:
      car.reset()
  
  def save_network(self, network:Network):
    network.save(f'models/{self.name}.pkl')
  
  def load_network(self, filename):
    self.population.pop()
    net = Network()
    net.load(filename)
    self.population.insert(0, net)


if __name__ == '__main__':
  p = Population("test", size=100)
  p.evolve()
  copy = Population("test", size=1, learning_rate=0, trained_model="models/test.pkl")
  copy.evolve()
