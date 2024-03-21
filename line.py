class Line(object):
  """Line class for mainly checking intercepts between lines"""
  def __init__(self, p1: tuple[int], p2: tuple[int], id: str = None) -> None:
    """__init__ uses points to save a Line

    Args:
        p1 (tuple[int]): first point 1
        p2 (tuple[int]): point 2
        id (str, optional): Identification. Defaults to None.
    """
    self.p1 = p1
    self.p2 = p2
    self.id = id

  def intercepts(self, second_line: object):
    """intercepts other line check

    Args:
        second_line (Line)

    Returns:
        tuple[float, tuple[float, float]]: distance, intercept point
    """
    x1, y1 = self.p1
    x2, y2 = self.p2
    x3, y3 = second_line.p1
    x4, y4 = second_line.p2
    # calculate the distance to intersection point
    denominator = ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

    if denominator == 0:
      return False

    uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denominator
    uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denominator
    
    # if uA and uB are between 0-1, lines are colliding
    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
      intersectionX = x1 + (uA * (x2-x1))
      intersectionY = y1 + (uA * (y2-y1))
      dist = ((intersectionX-x1)**2 + (intersectionY-y1)**2)**0.5
      return (dist, (intersectionX, intersectionY))
    return False