import json
from settings import *
import pygame as pg
from line import Line

class Environment:
  def __init__(self, filename="models/circuit.json") -> None:
    self.circuit_lines: list[Line] = []
    self.reward_gates: list[Line] = []
    self.polygons: list = []
    self.load(filename)
    
  def save(self, filename:str) -> None:
    reward_line_points = [(x.p1, x.p2) for x in self.reward_gates]
    circuit_line_points = [(x.p1, x.p2) for x in self.circuit_lines]
    polygons = self.polygons
    for polygon in self.polygons:
      points = [x[1:].split(", ") for x in polygon.split("),")]
      points = [tuple(map(int, x)) for x in points if len(x)!=1]
      polygons.append(points)

    params = {"reward": reward_line_points, "circuit": circuit_line_points, "polygons": polygons}
    with open(filename, 'w') as f:
      json.dump(params, f)

  def load(self, filename:str) -> None:
    with open(filename, 'r') as f:
      params: dict = json.load(f)
    self.reward_gates = [Line(x[0], x[1]) for x in params.get("reward")]
    self.circuit_lines = [Line(x[0], x[1]) for x in params.get("circuit")]
    self.polygons = params.get("polygons")
  
  def draw(self, screen, debug=True):
    for index, polygon in enumerate(self.polygons):
      clr = GREY if index == 0 else BACKGROUND_COLOR
      pg.draw.polygon(screen, clr, polygon)

    for line in self.circuit_lines:
      pg.draw.line(screen, WHITE, line.p1, line.p2)

    if not debug:
      return
    
    for line in self.reward_gates:
      pg.draw.line(screen, BLUE, line.p1, line.p2)
if __name__ == '__main__':
  """ Testing """
  e = Environment()
  e.load("models/circuit.json")
  # e.save("models/circuit.json")
  # e.draw(None)