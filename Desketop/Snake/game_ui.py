import pygame
from .settings import (
    WHITE, BLACK, LARGE_FONT_SIZE, FONT_SIZE,
    SCREEN_WIDTH, SCREEN_HEIGHT
)
from .high_scores import load_high_scores


class GameUI:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', FONT_SIZE)
        self.big_font = pygame.font.SysFont('Arial', LARGE_FONT_SIZE)

    def draw(self, surface, score, level, speed, paused=False, game_over=False, snake=None):
        # Dibujar puntuación, nivel y velocidad en la parte superior
        score_text = self.font.render(f'Puntos: {score}', True, WHITE)
        level_text = self.font.render(f'Nivel: {level}', True, WHITE)
        speed_text = self.font.render(f'Velocidad: {speed}', True, WHITE)

        surface.blit(score_text, (10, 10))
        surface.blit(level_text, (10, 40))
        surface.blit(speed_text, (10, 70))

        # Dibujar efectos activos si los hay
        if hasattr(snake, 'effects') and snake.effects:
            effects_text = "Efectos: " + ", ".join(snake.effects.keys())
            effects_surface = self.font.render(effects_text, True, (255, 255, 0))
            surface.blit(effects_surface, (10, 100))

        # Dibujar menú de pausa
        if paused:
            self._draw_centered_message(
                surface,
                'PAUSA',
                'Presiona P para continuar',
                'o R para reiniciar'
            )

        # Dibujar pantalla de fin de juego con puntuaciones
        if game_over:
            self._draw_game_over(surface, score)

    def _draw_game_over(self, surface, final_score):
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        # Título de fin de juego
        title = self.big_font.render('¡JUEGO TERMINADO!', True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title, title_rect)

        # Puntuación final
        score_text = self.font.render(f'Puntuación final: {final_score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
        surface.blit(score_text, score_rect)

        # Título de puntuaciones altas
        hs_title = self.font.render('Mejores Puntuaciones:', True, (255, 255, 0))
        hs_title_rect = hs_title.get_rect(center=(SCREEN_WIDTH // 2, 250))
        surface.blit(hs_title, hs_title_rect)

        # Cargar y mostrar puntuaciones altas
        high_scores = load_high_scores()
        for i, score in enumerate(high_scores[:5], 1):
            # Resaltar la puntuación actual si está entre las mejores
            color = (0, 255, 0) if score == final_score and score > 0 else WHITE
            hs_text = self.font.render(f"{i}. {score}", True, color)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, 290 + i * 30))
            surface.blit(hs_text, hs_rect)

        # Instrucciones
        restart_text = self.font.render("Presiona R para reiniciar", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        surface.blit(restart_text, restart_rect)

    def _draw_centered_message(self, surface, *lines):
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Dibujar cada línea de texto centrada
        for i, line in enumerate(lines):
            if i == 0:  # Primera línea en fuente grande
                text = self.big_font.render(line, True, WHITE)
            else:
                text = self.font.render(line, True, WHITE)

            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT // 2 + (i - len(lines) // 2) * 40)
            )
            surface.blit(text, text_rect)