import pygame
import os
from src.entities.player import Player
from src.engine.asset_manager import AssetManager
from src.engine.tilemap import Tilemap
from src.entities.plant import Plant

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.font = pygame.font.SysFont("Arial", 24)

        # Rozměry obrazovky
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Tilemap
        self.assets = AssetManager()
        self.tilemap = Tilemap(self.assets)

        # Hráč
        self.player = Player(100, 100, 40, 40, 5, self.screen_width, self.screen_height)

        # Cesty k ikonám
        asset_path = os.path.join(os.path.dirname(__file__), "..", "assets", "tiles")
        pause_icon_path = os.path.join(asset_path, "pause.png")
        quit_icon_path = os.path.join(asset_path, "quit.png")


        # Načtení a úprava ikon
        self.pause_icon = pygame.transform.scale(
            pygame.image.load(pause_icon_path).convert_alpha(), (32, 32)
        )
        self.quit_icon = pygame.transform.scale(
            pygame.image.load(quit_icon_path).convert_alpha(), (32, 32)
        )

        # Umístění ikon
        self.pause_button = self.pause_icon.get_rect(topright=(self.screen_width - 10, 10))
        self.quit_button = self.quit_icon.get_rect(topright=(self.screen_width - 10, 50))

        self.test_plant = Plant("carrot", (6, 6), self.assets.get_plant_images("carrot"))
        self.tilemap.add_plant(self.test_plant, (6, 6))

        self.obstacles = []

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

    def harvest_plant(self, pos):
        tile_pos = self.tilemap.pixel_to_tile_pos(pos)
        plant = self.tilemap.get_plant(tile_pos)
        if not plant:
            return
        if plant.ready_to_harvest():
            self.tilemap.harvest_plant(tile_pos)
            print("Harvested plant")

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = self.player.handle_input(keys)
        self.player.move(dx, dy, self.obstacles)
        if self.player.interacting:
            plant_loc = (self.player.rect.centerx, self.player.rect.bottom)
            self.harvest_plant(plant_loc)
        self.test_plant.update()

    def draw(self):
        self.tilemap.render(self.screen) # Tilemap - pozadí
        self.test_plant.render(self.screen)
        self.player.render(self.screen)

        # Info
        info = self.font.render(
            f"Level: {self.player.level}   EXP: {self.player.exp}/100", True, (117, 55, 19)
        )
        self.screen.blit(info, (10, 10))

        # Tlačítka
        self.screen.blit(self.pause_icon, self.pause_button)
        self.screen.blit(self.quit_icon, self.quit_button)

        # Pauzová zpráva
        if self.paused:
            paused_msg = self.font.render("PAUZA", True, (117, 55, 19))
            msg_rect = paused_msg.get_rect(center=(self.screen_width // 2, 40))
            self.screen.blit(paused_msg, msg_rect)
