import pygame
import os
from src.entities.player import Player

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.font = pygame.font.SysFont("Arial", 24)

        # Herní stav
        self.player = Player(100, 100, 40, 40)

        # Cesty k ikonám
        asset_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        pause_icon_path = os.path.join(asset_path, "pause.png")
        quit_icon_path = os.path.join(asset_path, "quit.png")

        # Načti a nastav ikonky
        self.pause_icon = pygame.image.load(pause_icon_path).convert_alpha()
        self.quit_icon = pygame.image.load(quit_icon_path).convert_alpha()

        self.pause_icon = pygame.transform.scale(self.pause_icon, (32, 32))
        self.quit_icon = pygame.transform.scale(self.quit_icon, (32, 32))

        # Obdélníky pro detekci kliknutí
        self.pause_button = self.pause_icon.get_rect(topright=(screen.get_width() - 10, 10))
        self.quit_button = self.quit_icon.get_rect(topright=(screen.get_width() - 10, 50))

    def run(self):
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_button.collidepoint(event.pos):
                    self.paused = not self.paused
                elif self.quit_button.collidepoint(event.pos):
                    self.running = False

        if not self.paused:
            keys = pygame.key.get_pressed()
            self.player.handle_movement(keys)

    def update(self):
        pass  # Herní logika

    def draw(self):
        self.screen.fill((34, 139, 34))  # pozadí

        # Postava
        pygame.draw.rect(
            self.screen, (139, 69, 19),
            (self.player.position_x, self.player.position_y, self.player.width, self.player.height)
        )

        # Info
        info = self.font.render(f"Level: {self.player.level}   EXP: {self.player.exp}/100", True, (255, 255, 255))
        self.screen.blit(info, (10, 10))

        # Tlačítka (ikonky)
        self.screen.blit(self.pause_icon, self.pause_button)
        self.screen.blit(self.quit_icon, self.quit_button)

        # Pauza text
        if self.paused:
            paused_msg = self.font.render("PAUSED", True, (255, 255, 255))
            msg_rect = paused_msg.get_rect(center=(self.screen.get_width() // 2, 40))
            self.screen.blit(paused_msg, msg_rect)
