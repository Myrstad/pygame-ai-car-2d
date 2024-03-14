from settings import *
from line import Line
from environment import Environment
import pygame as pg

def rotate_point(point, center, degrees) -> tuple[int]:
  p = pg.Vector2(point)
  c = pg.Vector2(center)
  p -= c
  p = p.rotate(degrees)
  p += c
  return (p.x, p.y)

class Car(object):
  def __init__(self, environment: Environment = Environment(), x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2) -> None:
    self.car_dim  = pg.Vector2(CAR_SIZE)
    self.direction = pg.Vector2(0, 1)
    self.start_position = (x, y)
    self.start_direction = (0, 1)
    self.center_position = pg.Vector2(x, y)
    self.velocity = pg.Vector2(0, 0)
    self.friction = CAR_FRICTION
    self.acceleration = CAR_ACCELERATION
    self.turning_speed = CAR_TURNING_SPEED
    self.environment = environment
    self.crashed = False
    self.sensor_directions = [0, -20, 20, 45, -45, 90,-90, 135, -135, 180]
    self.sensor_distance = 200
    self.current_reward_gate = 0

  def reset(self) -> None:
    self.crashed = False
    self.center_position.x = self.start_position[0]
    self.center_position.y = self.start_position[1]
    self.direction.x = self.start_direction[0]
    self.direction.y = self.start_direction[1]
    self.velocity *= 0


  def draw(self, surface, debug:bool = False):
    #draw "debug" lines
    if debug:
      sensor_vectors = [self.direction.rotate(x)*self.sensor_distance for x in self.sensor_directions]
      for vector in sensor_vectors:
        line = Line(self.center_position, self.center_position + vector)
        pg.draw.line(surface, BLACK, line.p1, line.p2)
        intercepts = []
        for env_line in self.environment.circuit_lines:
          if line.intercepts(env_line):
            intercepts.append(line.intercepts(env_line))
            # pg.draw.circle(surface, BLACK, line.intercepts(env_line)[1], 5)
        
        if len(intercepts) > 0:
          intercepts.sort(key=lambda x: x[0])
          pg.draw.circle(surface, BLACK, intercepts[0][1], 5)
    
    #draw car
    points = self.get_points()
    clr = RED if not self.crashed else BLUE
    pg.draw.polygon(surface, clr, points)

    #draw chevron in direction
    points = []
    w = self.car_dim[0] #width of car
    h = self.car_dim[1] #width of car
    cpx = self.center_position[0] #center position x
    cpy = self.center_position[1] #center position y
    rotation = self.direction.angle_to(pg.Vector2(1,0)) # degrees
    points = [(cpx, cpy-h//4), (cpx+w//3, cpy), (cpx, cpy+h//4)]
    points = [rotate_point(p, self.center_position, -rotation) for p in points]
    pg.draw.lines(surface, BLACK, False, points, 3)



  def get_points(self) -> list[tuple[int]]:
    rotation = self.direction.angle_to(pg.Vector2(1,0)) # degrees
    cpx = self.center_position.x
    cpy = self.center_position.y
    hw = self.car_dim[0] // 2
    hh = self.car_dim[1] // 2
    points = [(cpx-hw, cpy-hh), (cpx+hw, cpy-hh), (cpx+hw, cpy+hh), (cpx-hw, cpy+hh)] #tl, tr, br, bl

    points = [rotate_point(p, self.center_position, -rotation) for p in points]
    
    return points
  
  @staticmethod
  def make_lines(points:list[tuple[int]]) -> list[Line]:
    lines: list[Line] = []
    for index, point in enumerate(points):
      if index == 0:
        lines.append(Line(points[-1], point))
      else:
        lines.append(Line(lines[-1].p1, point))
    return lines


  def update(self, keys:dict):
    if (keys[pg.K_w] or keys[pg.K_UP]) and not self.crashed:
      self.velocity += self.direction * self.acceleration
    if (keys[pg.K_s] or keys[pg.K_DOWN]) and not self.crashed:
      self.velocity -= self.direction * self.acceleration
    if (keys[pg.K_a] or keys[pg.K_LEFT]) and not self.crashed:
      self.direction = self.direction.rotate(-self.turning_speed)
    if (keys[pg.K_d] or keys[pg.K_RIGHT]) and not self.crashed:
      self.direction = self.direction.rotate(self.turning_speed)
    if keys[pg.K_r]:
      self.reset()
    
    self.velocity *= self.friction
  
    self.center_position += self.velocity

    # check environment collisions
    points = self.get_points()
    lines = Car.make_lines(points)
    for car_line in lines:
      for env_line in self.environment.circuit_lines:
        if car_line.intercepts(env_line) != False:
          self.crashed = True
    
    #check reward gates
    for line in lines:
      if self.environment.reward_gates[self.current_reward_gate].intercepts(line) != False and not self.crashed:
        print(self.current_reward_gate, end="   ")
        self.current_reward_gate += 1
        if self.current_reward_gate == len(self.environment.reward_gates):
          self.current_reward_gate = 0
        print(self.current_reward_gate)
    

    #simple out of bounds (window) check
    if self.center_position.x < 0:
      self.center_position.x = 0
    if self.center_position.y < 0:
      self.center_position.y = 0
    if self.center_position.x > SCREEN_SIZE[0]:
      self.center_position.x = SCREEN_SIZE[0]
    if self.center_position.y > SCREEN_SIZE[1]:
      self.center_position.y = SCREEN_SIZE[1]