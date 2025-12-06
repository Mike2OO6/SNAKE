import random
import pygame
from .settings import (
    OBSTACLE_COLOR, BLACK, CELL_SIZE,
    GRID_SIZE, OBSTACLE_LIFETIME, WHITE,
    OBSTACLE_SHAPES
)


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.last_spawn_time = 0
        self.spawn_interval = 3000  # 3 segundos entre generación de obstáculos
        self.shape_functions = {
            'create_wall': self._create_wall,
            'create_divider': self._create_divider,
            'create_circle': self._create_circle,
            'create_cross': self._create_cross
        }

    def _create_wall(self, x, y, size=0):
        """Crea una pared que cruza todo el mapa"""
        wall_type = random.choice(['horizontal', 'vertical'])
        positions = []

        if wall_type == 'horizontal':
            # Pared horizontal completa
            for i in range(GRID_SIZE):
                positions.append((i, y))
        else:
            # Pared vertical completa
            for i in range(GRID_SIZE):
                positions.append((x, i))

        return positions

    def _create_divider(self, x, y, size=0):
        """Divide el mapa en 4 cuadrantes"""
        positions = []
        # Línea vertical central
        for i in range(GRID_SIZE):
            positions.append((GRID_SIZE // 2, i))
        # Línea horizontal central
        for i in range(GRID_SIZE):
            positions.append((i, GRID_SIZE // 2))
        return positions

    def _create_circle(self, x, y, size=3):
        """Crea un obstáculo circular"""
        positions = []
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                if i * i + j * j <= size * size:
                    positions.append((x + i, y + j))
        return positions

    def _create_cross(self, x, y, size=2):
        """Crea un obstáculo en forma de cruz"""
        positions = []
        for i in range(-size, size + 1):
            positions.append((x + i, y))  # Línea horizontal
            positions.append((x, y + i))  # Línea vertical
        return list(set(positions))

    def _is_position_valid(self, positions, snake_positions):
        """Verifica si las posiciones son válidas para colocar un obstáculo"""
        for x, y in positions:
            # Verificar límites del tablero
            if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
                return False
            # Verificar colisión con la serpiente
            if (x, y) in snake_positions:
                return False
        return True

    def update(self, snake):
        current_time = pygame.time.get_ticks()

        # Generar nuevos obstáculos
        if (current_time - self.last_spawn_time > self.spawn_interval and
                random.random() < 0.5):  # 50% de probabilidad de generar obstáculo

            # Elegir un tipo de obstáculo basado en las probabilidades
            shape_name, shape_data = random.choices(
                list(OBSTACLE_SHAPES.items()),
                weights=[s['spawn_chance'] for s in OBSTACLE_SHAPES.values()]
            )[0]

            shape_func = self.shape_functions[shape_data['function']]

            # Intentar colocar el obstáculo en una posición válida
            for _ in range(10):  # Intentar hasta 10 veces
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)

                # Obtener las posiciones que ocuparía el obstáculo
                obstacle_positions = shape_func(x, y)

                # Verificar si la posición es válida
                if self._is_position_valid(obstacle_positions, snake.positions):
                    # Añadir el obstáculo
                    self.obstacles.append({
                        'positions': obstacle_positions,
                        'spawn_time': current_time,
                        'shape': shape_name,
                        'color': shape_data['color'],
                        'duration': shape_data['duration']
                    })
                    break

            self.last_spawn_time = current_time

        # Eliminar obstáculos viejos
        current_time = pygame.time.get_ticks()
        self.obstacles = [
            obs for obs in self.obstacles
            if current_time - obs['spawn_time'] < obs['duration']
        ]

    def draw(self, surface):
        for obstacle in self.obstacles:
            for x, y in obstacle['positions']:
                rect = pygame.Rect(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                # Usar el color definido para este tipo de obstáculo
                pygame.draw.rect(surface, obstacle['color'], rect)
                pygame.draw.rect(surface, WHITE, rect, 1)  # Borde blanco

    def check_collision(self, position):
        """Verifica si una posición colisiona con algún obstáculo"""
        for obstacle in self.obstacles:
            if position in obstacle['positions']:
                return True
        return False