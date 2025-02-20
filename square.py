import pygame


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.background = pygame.surface.Surface([600, 600])
        self.background.fill((0, 0, 0))
        self.counter = 0
        self.shift_x = 0
        self.speed_x = 1
        self.shift_y = 0
        self.speed_y = 1
        self.dx = self.speed_x
        self.dy = self.speed_y
        self.is_work = True


    def horizontal_line(self):
        pygame.draw.line(self.screen,
                         (0, 255, 0, 0),
                         (150, 150 + self.shift_y),
                         (450, 150 + self.shift_y),
                         5)
        self.shift_y += self.dy
        if self.shift_y >= 300:
            self.dy = -self.speed_y
        if self.shift_y <= 0:
            self.dy = self.speed_y

        if self.counter < 10:
            self.counter += 1

    def horizontal_line2(self):
        pygame.draw.line(self.screen,
                         (0, 254, 0, 0),
                         (150, 150 + self.shift_y - self.counter),
                         (450, 150 + self.shift_y - self.counter),
                         5)
        self.shift_y += self.dy
        if self.shift_y >= 300:
            self.dy = -self.speed_y
        if self.shift_y <= 0:
            self.dy = self.speed_y

    def vertical_line(self):
        pygame.draw.line(self.screen,
                         (0, 255, 0),
                         (150 + self.shift_x, 150),
                         (150 + self.shift_x, 450),
                         5)
        self.shift_x += self.dy
        if self.shift_x >= 300:
            self.dx = -self.speed_x
        if self.shift_x <= 0:
            self.dx = self.speed_x

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        game.horizontal_line()
        game.horizontal_line2()
#        game.vertical_line()
        pygame.display.update()



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_work = False

    def run(self):
        while self.is_work:
            self.check_events()
            self.draw()
            pygame.time.delay(16)


game = Game()
game.run()
