# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
GRID_SIZE = SCREEN_WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 200, 0)
DARK_GRAY = (50, 50, 50)
GOLD = (255, 215, 0)
LIGHT_BLUE = (0, 191, 255)

# Snake settings
SNAKE_COLOR = GREEN
SNAKE_HEAD_COLOR = (0, 150, 0)
INITIAL_LENGTH = 5

# Game settings
INITIAL_SPEED = 10
MAX_SPEED = 30
BOOSTED_SPEED_MULTIPLIER = 2

# Food settings
FOOD_TYPES = {
    'normal': {
        'color': RED,
        'score': 10,
        'effect': None,
        'spawn_chance': 0.7,
        'duration': 0
    },
    'bonus': {
        'color': GOLD,
        'score': 30,
        'effect': 'grow',
        'spawn_chance': 0.2,
        'duration': 10000
    },
    'speed': {
        'color': LIGHT_BLUE,
        'score': 20,
        'effect': 'speed_boost',
        'spawn_chance': 0.1,
        'duration': 5000
    }
}

# Food spawn settings
FOOD_SPAWN_INTERVAL = 1000  # 1 segundo
MAX_FOOD_COUNT = 5  # Máximo de comidas en pantalla

# Obstacle settings
OBSTACLE_COLOR = (128, 128, 128)
OBSTACLE_SPAWN_RATE = 0.3
OBSTACLE_LIFETIME = 10000  # 10 segundos

# UI settings
FONT_SIZE = 24
LARGE_FONT_SIZE = 48
UI_COLOR = WHITE

# High scores
import os
HIGH_SCORES_FILE = os.path.join(os.path.dirname(__file__), 'high_scores.dat')

# Obstacle shapes
OBSTACLE_SHAPES = {
    'wall': {
        'function': 'create_wall',
        'size': 0,
        'color': (200, 50, 50),
        'duration': 8000,
        'spawn_chance': 0.1
    },
    'divider': {
        'function': 'create_divider',
        'size': 0,
        'color': (50, 50, 200),
        'duration': 5000,
        'spawn_chance': 0.1
    },
    'circle': {
        'function': 'create_circle',
        'size': 3,
        'color': (200, 200, 50),
        'duration': 10000,
        'spawn_chance': 0.2
    },
    'cross': {
        'function': 'create_cross',
        'size': 2,
        'color': (50, 200, 50),
        'duration': 7000,
        'spawn_chance': 0.2
    }
}