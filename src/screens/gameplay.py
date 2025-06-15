import pygame
import os
from src.entities.player import Player
from src.engine.asset_manager import AssetManager
from src.engine.tilemap import Tilemap
from src.entities.plant import Plant
from src.screens.rim import Rim

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.font = pygame.font.SysFont("Arial", 24)

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.assets = AssetManager()
        self.tilemap = Tilemap(self.assets)
        self.player = Player(100, 100, 40, 40, 5, self.screen_width, self.screen_height)

        # Lišta dole
        self.rim = Rim(self.screen_width, self.screen_height, self.font, self.player)
        self.obstacles = [self.rim.get_rect()]  # spodní lišta jako překážka

        # Rostlina
        self.test_plant = Plant("carrot", (6, 6), self.assets.get_plant_images("carrot"))
        self.tilemap.add_plant(self.test_plant, (6, 6))

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
                action = self.rim.handle_click(event.pos)
                if action == "pause":
                    self.paused = not self.paused
                elif action == "quit":
                    self.running = False

    def harvest_plant(self, pos):
        tile_pos = self.tilemap.pixel_to_tile_pos(pos)
        plant = self.tilemap.get_plant(tile_pos)
        if plant and plant.ready_to_harvest():
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
        self.tilemap.render(self.screen)
        self.test_plant.render(self.screen)
        self.player.render(self.screen)

        # Pauzová zpráva
        if self.paused:
            paused_msg = self.font.render("PAUZA", True, (117, 55, 19))
            msg_rect = paused_msg.get_rect(center=(self.screen_width // 2, 40))
            self.screen.blit(paused_msg, msg_rect)

        # Lišta
        self.rim.draw(self.screen)
