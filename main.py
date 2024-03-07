import pygame as pg
from settings import * 

def rotate_point(point, center, degrees) -> tuple[int]:
  p = pg.Vector2(point)
  c = pg.Vector2(center)
  p -= c
  p = p.rotate(degrees)
  p += c
  return (p.x, p.y)
  


class Car(object):
  def __init__(self) -> None:
    self.car_dim  = pg.Vector2(CAR_SIZE)
    self.direction = pg.Vector2(1, 0)
    self.center_position = pg.Vector2(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
    self.velocity = pg.Vector2(0, 0)
    self.friction = 0.975

  def draw(self, surface):
    rotation = self.direction.angle_to(pg.Vector2(1,0)) # degrees
    cpx = self.center_position.x
    cpy = self.center_position.y
    hw = self.car_dim[0] // 2
    hh = self.car_dim[1] // 2
    points = [(cpx-hw, cpy-hh), (cpx+hw, cpy-hh), (cpx+hw, cpy+hh), (cpx-hw, cpy+hh)] #tl, tr, br, bl

    points = [rotate_point(p, self.center_position, -rotation) for p in points]

    pg.draw.polygon(surface, RED, points)

  def update(self, keys:dict):
    if keys[pg.K_w] or keys[pg.K_UP]:
      self.velocity += self.direction * 0.3
    if keys[pg.K_s] or keys[pg.K_DOWN]:
      self.velocity -= self.direction * 0.3
    if keys[pg.K_a] or keys[pg.K_LEFT]:
      self.direction = self.direction.rotate(-3)
    if keys[pg.K_d] or keys[pg.K_RIGHT]:
      self.direction = self.direction.rotate(3)
    
    self.velocity *= self.friction

    self.center_position += self.velocity

    #simple out of bounds check
    if self.center_position.x < 0:
      self.center_position.x = 0
    if self.center_position.y < 0:
      self.center_position.y = 0
    if self.center_position.x > screen.get_width():
      self.center_position.x = screen.get_width()
    if self.center_position.y > screen.get_height():
      self.center_position.y = screen.get_height()


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
  