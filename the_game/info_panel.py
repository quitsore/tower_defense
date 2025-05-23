import math

import pygame


class InfoPanel:
    def __init__(self, player):
        self.prep_time = 10
        self.prep_counter = 60
        self.start_angle = math.radians(90)
        self.end_angle = self.start_angle + math.radians(360)
        self.speed = math.radians(0.6)
        self.text_font = pygame.font.SysFont("Arial", 30)
        self.player_gold = None
        self.player = player

    def action(self):
        pass

    def draw(self, screen):
        if self.prep_counter != 0:
            self.prep_counter -= 1
        else:
            self.prep_counter = 60
            if self.prep_time != 0:
                self.prep_time -= 1

        self._draw_text(screen, f"{self.prep_time}", self.text_font, (255, 255, 255), 1040, 540)
        if self.end_angle > self.start_angle:
            pygame.draw.arc(screen, (255, 255, 255), pygame.Rect(1025, 525, 60, 60), self.start_angle,
                            self.end_angle, 3)
            self.start_angle += self.speed

        self._draw_text(screen, f"Gold: {self.player.gold}", self.text_font, (255, 255, 255), 1040, 640)

    @staticmethod
    def _draw_text(screen, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
