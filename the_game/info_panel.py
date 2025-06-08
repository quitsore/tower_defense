import datetime
import logging
import math

import pygame


class InfoPanel:
    def __init__(self, player, screen):
        self.screen = screen
        self.start_angle = math.radians(90)
        self.end_angle = self.start_angle + math.radians(360)
        self.text_font = pygame.font.Font("../resources/MotionControl-Bold.otf", 36)
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
            logging.debug(f"remaining_time: {self.remaining_time}")
            self.start_angle = math.radians(90 + (360 - 360 * self.remaining_time / self.total_duration))
            return False
        else:
            return True

    def draw(self, screen):
        if self.remaining_time.days >= 0:
            remaining_time_seconds = self.remaining_time.seconds + 1
        else:
            remaining_time_seconds = 0
        self._draw_text(screen, f"{remaining_time_seconds}", self.text_font, (255, 255, 255), 1040, 540)
        if self.end_angle > self.start_angle:
            pygame.draw.arc(screen, (255, 255, 255), pygame.Rect(1012, 510, 60, 60), self.start_angle,
                            self.end_angle, 3)
        self._draw_text(screen, f"Gold: {self.player.gold}", self.text_font, (255, 255, 255), 1040, 640)

    @staticmethod
    def _draw_text(screen, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img_rect = img.get_rect(center=(x, y))
        screen.blit(img, (img_rect.x, img_rect.y))
