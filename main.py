import pygame as pg
from settings import * 
from environment import Environment
from population import Population

def main():
  pg.init()
  screen = pg.display.set_mode(SCREEN_SIZE)
  clock = pg.time.Clock()

  debugging = False

  p = Population(CURRENT_MODEL_NAME, size=POPULATION_SIZE, learning_rate=LEARNING_RATE, trained_model=TRAINED_MODEL_PATH)

  environment = Environment(ENVIRONMENT_PATH)
  # car = Car(environment, 110, 400)

  running = True
  while running:
    clock.tick(FPS)

    for event in pg.event.get():
      if event.type == pg.QUIT:
        running = False
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          running = False
        if event.key == pg.K_b:
          debugging = not debugging
        if event.key == pg.K_k:
          for car in p.cars:
            car.crashed = True

    keys_pressed = pg.key.get_pressed()
    # car.update(keys_pressed)

    for index, c in enumerate(p.cars):
      if not c.crashed:
        c.update(keys_pressed, [float(x) for x in p.population[index].forward(c.get_neural_network_input())[0]])
      else:
        c.update(keys_pressed)

    #rendering
    screen.fill(BACKGROUND_COLOR)
    environment.draw(screen, debug=debugging)
    # car.draw(screen, debug=debugging)
    for c in p.cars:
      c.draw(screen, debug=False)
    
    # if all cars are dead
    # print([car.crashed for car in p.cars].count(False))
    if [car.crashed for car in p.cars].count(False) == 0:
      # print([car.fitness for car in p.cars])
      # p.evolve()
      [car.fitness for car in p.cars]
      p.evolve()

    #update screen
    pg.display.flip()

  pg.quit()

if __name__ == '__main__':
  main()