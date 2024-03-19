from settings import *
from line import Line
from car import Car
from environment import Environment
import pygame as pg

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(SCREEN_SIZE)
prev_mouse_position = None
env = Environment(filename=None)
car = Car(env)

outer_lines: list[Line] = []
inner_lines: list[Line] = []
start_position = None
point_from_start_towards_direction = None
reward_gates: list[Line] = []

current_mode: int | str = "p" # 1 (inner), 2(outer), "p"(start point), "d"(point to get direction, also need p), "m"(profit; reward gates)


running = True
while running:
  clock.tick(FPS)
  screen.fill(BACKGROUND_COLOR)
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_p:
        current_mode = "p"
      if event.key == pg.K_d:
        current_mode = "d"
      if event.key == pg.K_m:
        current_mode = "r"
        prev_mouse_position = None
      if event.key == pg.K_1:
        current_mode = 1
        prev_mouse_position = None
      if event.key == pg.K_2:
        current_mode = 2
        prev_mouse_position = None
      if event.key == pg.K_s:
        polygons = []
        points = []
        for index, line in enumerate(outer_lines):
          if index == 0:
            points.append(line.p2)
          points.append(line.p1)
        polygons.append(points)
        points = []
        for index, line in enumerate(inner_lines):
          if index == 0:
            points.append(line.p2)
          points.append(line.p1)
        polygons.append(points)
        env.polygons = polygons
        env.save("models/snake.json")

    if event.type == pg.MOUSEBUTTONDOWN:
      if current_mode == "p":
        start_position = event.pos
        env.start_position = start_position
        print(start_position)
      if current_mode == 'd' and env.start_position:
        point_from_start_towards_direction = event.pos
        p1 = start_position
        p2 = point_from_start_towards_direction
        env.start_direction = pg.Vector2(p2[0]-p1[0], p2[1]-p1[1]).normalize()
      if current_mode == 1:
        if prev_mouse_position == None:
          prev_mouse_position = event.pos
          continue
        outer_lines.append(Line(event.pos, prev_mouse_position))
        prev_mouse_position = event.pos
      if current_mode == 2:
        if prev_mouse_position == None:
          prev_mouse_position = event.pos
          continue
        inner_lines.append(Line(event.pos, prev_mouse_position))
        prev_mouse_position = event.pos
      if current_mode == "r":
        if prev_mouse_position == None:
          prev_mouse_position = event.pos
          continue
        reward_gates.append(Line(prev_mouse_position, event.pos))
        prev_mouse_position = None
          

  keys_pressed = pg.key.get_pressed()
  env.circuit_lines = []
  env.reward_gates = reward_gates
  [env.circuit_lines.append(x) for x in inner_lines]
  [env.circuit_lines.append(x) for x in outer_lines]
  car.update(keys_pressed)
  env.draw(screen, debug=True)
  if point_from_start_towards_direction:
    pg.draw.line(screen, WHITE, env.start_position, point_from_start_towards_direction, 2)
  car.draw(screen)

  pg.display.flip()
pg.quit()
exit()


