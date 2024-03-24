# display settings
SCREEN_SIZE = (800, 600)
FPS = 60

# car settings
CAR_SIZE = (30, 18)
CAR_FRICTION = 0.95
CAR_ACCELERATION = 0.3
CAR_TURNING_SPEED = 5

# colors
WHITE = (255, 255, 255)
BLACK = (0  , 0  , 0  )
GREY  = (127, 127, 127)
RED   = (255, 0  , 0  )
BLUE  = (0  , 0  , 255)
GREEN = (127, 200, 63 )

BACKGROUND_COLOR = GREEN

# Machine learning settings
ENVIRONMENT_PATH = "models/simple_opp.json"
TRAINED_MODEL_PATH = "models/simple_opp.pkl"
CURRENT_MODEL_NAME = "circuit"
LEARNING_RATE = 0 #0 is none, and does not save model
POPULATION_SIZE = 1