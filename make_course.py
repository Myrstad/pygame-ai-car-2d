from settings import *
from line import Line
from car import Car
from environment import Environment
import pygame as pg

lines: list[Line] = []

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(SCREEN_SIZE)
p1 = None
p2 = None
figure_index = 0
env = Environment()
car = Car(env, 110, 440)


running = True
while running:
  clock.tick(FPS)
  screen.fill(BLACK)
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_z:
        txt = ""
        prev_fig_idx = 0
        for line in lines:
          idx = line.id
          if idx != prev_fig_idx:
            txt = txt[:-1]
            txt += f'\n{line.p1},{line.p2},'
          else:
            txt += f'{line.p2},'

          prev_fig_idx = line.id
        with open("rewardgates.txt", 'w') as file:
          file.write(txt[:-1])

    if event.type == pg.MOUSEBUTTONDOWN:
      if not p1:
        p1 = event.pos
        print(p1)
      else:
        p2 = event.pos
        lines.append(Line(p1, p2, figure_index))
        print(p1, p2)
        p1 = lines[-1].p2
  
  keys_pressed = pg.key.get_pressed()
  car.update(keys_pressed)
  if keys_pressed[pg.K_SPACE]:
    p1 = None
    p2 = None
    figure_index += 1
  if keys_pressed[pg.K_r]:
    p1 = None
    p2 = None
    lines.clear()
    figure_index = 0

  env.draw(screen)
  car.draw(screen)
  for line in lines:
    pg.draw.line(screen, BLUE, line.p1, line.p2)
  pg.display.flip()
pg.quit()
exit()


