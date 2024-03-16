import json
from settings import *
import pygame as pg
from line import Line

class Environment:
  def __init__(self, filename="models/circuit.json") -> None:
    self.circuit_lines: list[Line] = []
    self.reward_gates: list[Line] = []
    self.polygons: list = []
    self.start_position = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
    self.start_direction: pg.Vector2 = pg.Vector2(0, 1) #should be normalized
    if filename:
      self.load(filename)
  
  def reset(self):
    self.circuit_lines = []
    self.reward_gates = []
    self.polygons = []

  def save(self, filename:str) -> None:
    reward_line_points = [(x.p1, x.p2) for x in self.reward_gates]
    circuit_line_points = [(x.p1, x.p2) for x in self.circuit_lines]
    polygons = self.polygons
    direction = [self.start_direction.x, self.start_direction.y]

    params = {"reward": reward_line_points, "circuit": circuit_line_points, "polygons": polygons, "position": self.start_position, "direction": direction}
    with open(filename, 'w') as f:
      json.dump(params, f, indent=2)

  def load(self, filename:str) -> None:
    with open(filename, 'r') as f:
      params: dict = json.load(f)
    self.reward_gates = [Line(x[0], x[1]) for x in params.get("reward")]
    self.circuit_lines = [Line(x[0], x[1]) for x in params.get("circuit")]
    self.polygons = params.get("polygons")
    if params.get("direction"):
      self.start_direction = pg.Vector2(params.get("direction"))
    if params.get("position"):
      self.start_position = params.get("position")
  
  def draw(self, screen, debug=True):
    for index, polygon in enumerate(self.polygons):
      clr = GREY if index == 0 else BACKGROUND_COLOR
      pg.draw.polygon(screen, clr, polygon)

    for line in self.circuit_lines:
      pg.draw.line(screen, WHITE, line.p1, line.p2)

    if not debug:
      return
    
    pg.draw.circle(screen, RED, self.start_position, 5)

    for line in self.reward_gates:
      pg.draw.line(screen, BLUE, line.p1, line.p2)
if __name__ == '__main__':
  """ Testing """
  e = Environment("models/test.json")
  # e.save("models/test.json")
  print(e.__dict__)
  screen = pg.display.set_mode(SCREEN_SIZE)
  e.draw(screen)
  # e.save("models/test.json")
  # e.save("models/circuit.json")
  # e.draw(None)