import random
import pygame
from .settings import FOOD_TYPES, GRID_SIZE, CELL_SIZE, WHITE, MAX_FOOD_COUNT


class FoodManager:
    def __init__(self, snake):
        self.foods = []
        self.snake = snake
        self.last_spawn_time = 0
        self.spawn_interval = 1000  # 1 segundo
        self.max_food = MAX_FOOD_COUNT

    def update(self):
        current_time = pygame.time.get_ticks()

        # Generar nueva comida periódicamente
        if (len(self.foods) < self.max_food and
                current_time - self.last_spawn_time > self.spawn_interval):
            self.foods.append(self._create_food())
            self.last_spawn_time = current_time

        # Actualizar estado de las comidas
        current_time = pygame.time.get_ticks()
        self.foods = [food for food in self.foods if not food.is_expired()]

    def _create_food(self):
        return Food(self.snake, self)

    def get_collided_food(self, position):
        """Devuelve la comida con la que colisionó la serpiente, o None"""
        for i, food in enumerate(self.foods):
            if food.position == position:
                return self.foods.pop(i)
        return None

    def draw(self, surface):
        for food in self.foods:
            food.draw(surface)


class Food:
    def __init__(self, snake, manager):
        self.snake = snake
        self.manager = manager
        self.type = self.choose_food_type()
        self.color = self.type['color']
        self.position = self.generate_position()
        self.spawn_time = pygame.time.get_ticks()
        self.duration = self.type.get('duration', 0)

    def choose_food_type(self):
        rand = random.random()
        cumulative = 0
        for food_type, props in FOOD_TYPES.items():
            cumulative += props['spawn_chance']
            if rand <= cumulative:
                return {**props, 'name': food_type}
        return {**FOOD_TYPES['normal'], 'name': 'normal'}

    def generate_position(self):
        while True:
            position = (
                random.randint(0, GRID_SIZE - 1),
                random.randint(0, GRID_SIZE - 1)
            )
            # Verificar que no esté en la serpiente ni en otra comida
            if (position not in self.snake.positions and
                    position not in [f.position for f in self.manager.foods]):
                return position

    def is_expired(self):
        if self.duration == 0:  # La comida normal no expira
            return False
        return (pygame.time.get_ticks() - self.spawn_time) > self.duration

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * CELL_SIZE,
            self.position[1] * CELL_SIZE,
            CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)

        # Mostrar temporizador para comidas especiales
        if self.duration > 0:
            time_left = (self.duration - (pygame.time.get_ticks() - self.spawn_time)) / 1000
            if time_left > 0:
                font = pygame.font.SysFont('Arial', 12)
                text = font.render(f"{time_left:.1f}s", True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                surface.blit(text, text_rect)