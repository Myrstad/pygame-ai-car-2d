import pygame as pg
from settings import * 
from car import Car
from environment import Environment
from line import Line

if __name__ == '__main__':
  pg.init()
  screen = pg.display.set_mode(SCREEN_SIZE)
  clock = pg.time.Clock()

  velocity = pg.Vector2()
  direction = pg.Vector2(0,1) #right
  position = pg.Vector2(SCREEN_SIZE[0] // 2 - CAR_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - CAR_SIZE[1] // 2)
  friction = 0.975
  debugging = False

  environment = Environment()
  car = Car(environment, 110, 400)

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

    keys_pressed = pg.key.get_pressed()
    car.update(keys_pressed)

    #rendering
    screen.fill(BACKGROUND_COLOR)
    environment.draw(screen, debug=debugging)
    car.draw(screen, debug=debugging)
    #update screen
    pg.display.flip()

  pg.quit()