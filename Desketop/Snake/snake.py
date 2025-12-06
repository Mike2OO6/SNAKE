import pygame
from .settings import (
    GRID_SIZE, SNAKE_COLOR, SNAKE_HEAD_COLOR,
    BLACK, CELL_SIZE, INITIAL_SPEED, INITIAL_LENGTH
)


class Snake:
    def __init__(self):
        # Inicializar con 5 segmentos
        start_x = GRID_SIZE // 2
        start_y = GRID_SIZE // 2
        self.positions = [(start_x - i, start_y) for i in range(INITIAL_LENGTH)]
        self.direction = (1, 0)
        self.color = SNAKE_COLOR
        self.head_color = SNAKE_HEAD_COLOR
        self.base_speed = INITIAL_SPEED
        self.boosted_speed = INITIAL_SPEED * 2
        self.speed = self.base_speed
        self.length = INITIAL_LENGTH
        self.score = 0
        self.effects = {}

    def get_head_position(self):
        return self.positions[0]

    def update_effects(self):
        current_time = pygame.time.get_ticks()
        # Eliminar efectos expirados
        self.effects = {
            effect: end_time
            for effect, end_time in self.effects.items()
            if end_time > current_time
        }

        # Aplicar efectos activos
        if 'speed_boost' in self.effects:
            self.speed = self.boosted_speed
        else:
            self.speed = self.base_speed

    def add_effect(self, effect_name, duration):
        """Añadir un efecto a la serpiente"""
        self.effects[effect_name] = pygame.time.get_ticks() + duration

    def move(self):
        self.update_effects()

        cur = self.positions[0]
        x = (cur[0] + self.direction[0]) % GRID_SIZE
        y = (cur[1] + self.direction[1]) % GRID_SIZE
        new_pos = (x, y)

        # Verificar colisión consigo misma
        if new_pos in self.positions[1:]:
            return False

        self.positions.insert(0, new_pos)
        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def grow(self, amount=1):
        self.length += amount
        self.score += 10 * amount

    def render(self, surface):
        for i, p in enumerate(self.positions):
            rect = pygame.Rect(
                p[0] * CELL_SIZE,
                p[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            color = self.head_color if i == 0 else self.color
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)