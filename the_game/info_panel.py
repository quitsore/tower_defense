import datetime
import logging
import math

import pygame


class InfoPanel:
    def __init__(self, player):
        self.start_angle = math.radians(90)
        self.end_angle = self.start_angle + math.radians(360)
        self.text_font = pygame.font.SysFont("Arial", 30)
        self.player_gold = None
        self.player = player
        self.start_time = datetime.datetime.now()
        self.total_duration = datetime.timedelta(days=-1)
        self.remaining_time = datetime.timedelta(days=-1)

    def init_counter(self, new_duration_s):
        self.start_time = datetime.datetime.now()
        self.total_duration = datetime.timedelta(seconds=new_duration_s)
        self.remaining_time = self.total_duration
        self.start_angle = math.radians(90)
        self.end_angle = self.start_angle + math.radians(360)

    def action(self):
        if self.remaining_time.days >= 0:
            now = datetime.datetime.now()
            self.remaining_time = self.start_time + self.total_duration - now
            logging.info(f"remaining_time: {self.remaining_time}")
            self.start_angle = math.radians(90 + (360 - 360 * self.remaining_time / self.total_duration))

    def draw(self, screen):
        if self.remaining_time.days >= 0:
            remaining_time_seconds = self.remaining_time.seconds + 1
        else:
            remaining_time_seconds = 0
        self._draw_text(screen, f"{remaining_time_seconds}", self.text_font, (255, 255, 255), 1040, 540)
        if self.end_angle > self.start_angle:
            pygame.draw.arc(screen, (255, 255, 255), pygame.Rect(1025, 525, 60, 60), self.start_angle,
                            self.end_angle, 3)
        self._draw_text(screen, f"Gold: {self.player.gold}", self.text_font, (255, 255, 255), 1040, 640)

    @staticmethod
    def _draw_text(screen, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
