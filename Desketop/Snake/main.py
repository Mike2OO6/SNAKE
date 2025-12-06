import os
import sys
import pygame
from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE,
    BLACK, DARK_GRAY, MAX_SPEED
)
from game.snake import Snake
from game.food import FoodManager
from game.obstacles import ObstacleManager
from game.game_ui import GameUI
from game.high_scores import update_high_scores


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food_manager = FoodManager(self.snake)
        self.obstacles = ObstacleManager()
        self.ui = GameUI()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    continue

                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_r and self.paused:
                    self.reset_game()

                if not self.paused and not self.game_over:
                    if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                        self.snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                        self.snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                        self.snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                        self.snake.direction = (1, 0)

        return True

    def update(self):
        if self.paused or self.game_over:
            return

        # Actualizar comida
        self.food_manager.update()

        # Mover serpiente
        if not self.snake.move():
            self.game_over = True
            update_high_scores(self.score)
            return

        # Verificar colisión con la comida
        head_pos = self.snake.get_head_position()
        eaten_food = self.food_manager.get_collided_food(head_pos)

        if eaten_food:
            # Aplicar efectos de la comida
            if eaten_food.type['effect'] == 'grow':
                self.snake.grow(3)
            elif eaten_food.type['effect'] == 'speed_boost':
                self.snake.add_effect('speed_boost', 5000)

            self.score += eaten_food.type['score']

            # Subir de nivel cada 50 puntos
            if self.score % 50 == 0:
                self.level += 1
                self.snake.base_speed = min(20, self.snake.base_speed + 1)
                self.snake.boosted_speed = self.snake.base_speed * 2

        # Actualizar obstáculos
        self.obstacles.update(self.snake)

        # Verificar colisión con obstáculos
        if self.obstacles.check_collision(self.snake.get_head_position()):
            self.game_over = True
            update_high_scores(self.score)
            return

    def draw(self):
        self.screen.fill(BLACK)

        # Dibujar cuadrícula
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (SCREEN_WIDTH, y))

        # Dibujar objetos del juego
        self.snake.render(self.screen)
        self.food_manager.draw(self.screen)
        self.obstacles.draw(self.screen)

        # Dibujar interfaz de usuario
        self.ui.draw(
            self.screen,
            self.score,
            self.level,
            self.snake.speed,
            self.paused,
            self.game_over,
            self.snake
        )

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()  # handle_events ahora retorna False para salir
            self.update()
            self.draw()
            self.clock.tick(self.snake.speed)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Añadir el directorio actual al path para importaciones
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    game = Game()
    game.run()
