import pygame as pg
from settings import * 
from car import Car

class Line(object):
  def __init__(self, p1:tuple[int], p2:tuple[int], id=None) -> None:
    self.p1 = p1
    self.p2 = p2
    self.id = id

  def intercepts(self, other:object):
    x1, y1 = self.p1
    x2, y2 = self.p2
    x3, y3 = other.p1
    x4, y4 = other.p2

    # calculate the distance to intersection point
    uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    
    # if uA and uB are between 0-1, lines are colliding
    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
      intersectionX = x1 + (uA * (x2-x1))
      intersectionY = y1 + (uA * (y2-y1))
      dist = ((intersectionX-x1)**2 + (intersectionY-y1)**2)**0.5
      return (dist, (intersectionX, intersectionY))
    return False

if __name__ == '__main__':
  pg.init()
  screen = pg.display.set_mode(SCREEN_SIZE)
  clock = pg.time.Clock()

  velocity = pg.Vector2()
  direction = pg.Vector2(0,1) #right
  position = pg.Vector2(SCREEN_SIZE[0] // 2 - CAR_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - CAR_SIZE[1] // 2)
  friction = 0.975

  car = Car()

  running = True
  while running:
    clock.tick(FPS)

    for event in pg.event.get():
      if event.type == pg.QUIT:
        running = False

    keys_pressed = pg.key.get_pressed()
    car.update(keys_pressed)

    #rendering
    screen.fill(BLACK)

    car.draw(screen)
    #update screen
    pg.display.flip()

  pg.quit()

  l1 = Line((20,20), (530,360))
  l2 = Line((210,240), (580,110))
  print(l1.intercepts(l2))