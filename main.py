import pygame as pg
from settings import * 
from car import Car
from environment import Environment
from population import Population

if __name__ == '__main__':
  pg.init()
  screen = pg.display.set_mode(SCREEN_SIZE)
  clock = pg.time.Clock()

  velocity = pg.Vector2()
  direction = pg.Vector2(0,1) #right
  position = pg.Vector2(SCREEN_SIZE[0] // 2 - CAR_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - CAR_SIZE[1] // 2)
  friction = 0.975
  debugging = False

  p = Population("showcase", size=50, learning_rate=0.1)

  environment = Environment("models/snake.json")
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