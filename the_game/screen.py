import pygame
from map import Map


class Game:

    def __init__(self):
        self.fps = None
        self.background = None
        pygame.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("game")
        self.path = pygame.image.load("../resources/path-32x40.png").convert()
        self.grass = pygame.image.load("../resources/grass-32x40.png").convert()
        self.placement = pygame.image.load("../resources/brick-32x40.png").convert()
        self.tower_shop = pygame.image.load("../resources/tower-32x40.png").convert()
        self.text_font = pygame.font.SysFont("Arial", 30)
        self.cursorPX, self.curserPY = self.width // 2, self.height // 2
        self.clock = pygame.time.Clock()
        self.x = 0
        self.y = 0
        self.is_work = True
        self.FPS = 60
        self.game_map = Map("terrain.txt")

    def draw_cursor(self, x, y):
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 20, 1)
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1, 1)
        pygame.draw.line(self.screen, (255, 255, 255), (x - 24, y),
                         (x - 16, y))
        pygame.draw.line(self.screen, (255, 255, 255), (x + 24, y),
                         (x + 16, y))
        pygame.draw.line(self.screen, (255, 255, 255), (x, y - 24),
                         (x, y - 16))
        pygame.draw.line(self.screen, (255, 255, 255), (x, y + 24),
                         (x, y + 16))

    def draw(self):
        self.background = pygame.surface.Surface([self.width, self.height])
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.draw_map()
        self.draw_square()

        show_fps = self.text_font.render(str(self.fps), True, (255, 255, 255))
        self.screen.blit(show_fps, (0, 0))

        self.draw_text("Shop", self.text_font, (255, 255, 255), 1050, 50)
        self.draw_text("Archer", self.text_font, (255, 255, 255), 1030, 200)
        self.draw_text("Mortar", self.text_font, (255, 255, 255), 1150, 200)
        self.draw_text("Ballista", self.text_font, (255, 255, 255), 1030, 350)
        self.draw_text("Freezer", self.text_font, (255, 255, 255), 1150, 350)
        pygame.draw.line(self.screen, (255, 255, 255), (1024, 100), (1280, 100))
        self.cursorPX, self.curserPY = pygame.mouse.get_pos()
        self.draw_cursor(self.cursorPX, self.curserPY)
        pygame.display.flip()
        pygame.display.update()

    def check_events(self):
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_work = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                btn = pygame.mouse
                print("x = {}, y = {}".format(pos[0], pos[1]))

    def run(self):
        while self.is_work:
            self.check_events()
            self.draw()
            self.clock.tick(self.FPS)
            self.fps = int(self.clock.get_fps())

    def draw_square(self):
        color = pygame.Color(255, 0, 0, 255)
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(self.x, self.y, 40, 40))
        self.x += 1.28
        self.y += 0.72

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_map(self):
        color = None
        for row_idx, row in enumerate(self.game_map.map):
            for col_idx, cell in enumerate(row):
                if cell == Map.FREE:
                    self.screen.blit(self.path, (col_idx * 32, row_idx * 40))
                elif cell == Map.TERRAIN:
                    self.screen.blit(self.grass, (col_idx * 32, row_idx * 40))
                elif cell == Map.TOWER:
                    self.screen.blit(self.placement, (col_idx * 32, row_idx * 40))
                elif cell == Map.CASTLE:
                    color = pygame.Color(255, 215, 0, 255)
                    pygame.draw.rect(self.screen, color,
                                     pygame.Rect(col_idx * 32, row_idx * 40, 32, 40))
                elif cell == Map.SHOP:
                    color = pygame.Color(0, 0, 0, 255)
                    pygame.draw.rect(self.screen, color,
                                     pygame.Rect(col_idx * 32, row_idx * 40, 32, 40))
                elif cell == 8:
                    self.screen.blit(self.tower_shop, (col_idx * 32, 160))
                if cell == Map.BOT:
                    color = pygame.Color(93, 93, 93, 255)
                    pygame.draw.rect(self.screen, color,
                                     pygame.Rect(col_idx * 40, row_idx * 40, 40, 40))

    def draw_shop(self):
        pass

game = Game()
game.run()
