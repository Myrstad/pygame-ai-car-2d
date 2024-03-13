from settings import *
import pygame as pg
from line import Line

class Environment:
  def __init__(self, path="environment.txt", reward_path="rewardgates.txt") -> None:
    with open(path) as file:
      raw = file.read()
    self.polygons = raw.split("\n")
    self.lines: list[Line] = []
    # print(self.polygons)
    for polygon in self.polygons:
      points = [x[1:].split(", ") for x in polygon.split("),")]
      points = [tuple(map(int, x)) for x in points if len(x)!=1]
      for index, point in enumerate(points):
        if index == 0:
          continue
        if index == 1:
          self.lines.append(Line(points[0], point))
        else:
          self.lines.append(Line(self.lines[-1].p2, point))
    
    # invisible reward gates
    self.reward_gates: list[Line] = []
    with open(reward_path) as file:
      raw = file.read()
    for id, gate in enumerate(raw.split("\n")):
      points = [x[1:].split(", ") for x in gate.split("),")]
      points=[tuple(map(int, x)) for x in points if len(x)!=1]
      p1,p2 = points
      self.reward_gates.append(Line(p1, p2, id))
    


  
  def draw(self, screen, debug=True):
    for index, polygon in enumerate(self.polygons):
      points = [x[1:].split(", ") for x in polygon.split("),")]
      points = [tuple(map(int, x)) for x in points if len(x)!=1]
      clr = GREY if index == 0 else BACKGROUND_COLOR
      pg.draw.polygon(screen, clr, points)

    for line in self.lines:
      pg.draw.line(screen, WHITE, line.p1, line.p2)

    if not debug:
      return
    
    for line in self.reward_gates:
      pg.draw.line(screen, BLUE, line.p1, line.p2)
if __name__ == '__main__':
  """ Testing """
  e = Environment()
  # e.draw(None)