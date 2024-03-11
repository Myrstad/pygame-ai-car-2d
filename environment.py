from settings import *
import pygame as pg

class Environment:
  def __init__(self, path="environment.txt") -> None:
    with open(path) as file:
      raw = file.read()
    self.polygons = raw.split("\n")
    print(self.polygons)
  
  def draw(self, screen):
    for polygon in self.polygons:
      points = [x[1:].split(", ") for x in polygon.split("),")]
      points = [tuple(map(int, x)) for x in points if len(x)!=1]
      pg.draw.polygon(screen, WHITE, points, 1)

if __name__ == '__main__':
  e = Environment()
  e.draw(None)