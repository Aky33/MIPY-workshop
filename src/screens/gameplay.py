import pygame
from src.entities.player import Player

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 24)

        # Herní stav
        self.player = Player(100, 100, 40, 40, 4)

    def run(self):
        while self.running:
            self.handle_events()
            #self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        dx, dy = self.player.handle_input(keys)
        self.player.move(dx, dy, [])

    def draw(self):
        self.screen.fill((34, 139, 34))  # zelená zahrada

        # Zahradník (čtverec)
        self.player.draw(self.screen)

        # Info panel
        info = self.font.render(f"Level: {self.player.level}   EXP: {self.player.exp}/100", True, (255, 255, 255))
        self.screen.blit(info, (10, 10))
