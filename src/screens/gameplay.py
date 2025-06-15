import pygame
import os
from src.entities.player import Player
from src.engine.asset_manager import AssetManager
from src.engine.tilemap import Tilemap
from src.entities.plant import Plant
from src.entities.carrot import Carrot
from src.entities.wheat import Wheat
from src.screens.rim import Rim
from src.gameplay.inventory import Inventory
from src.screens.inventory_interface import InventoryInterface
from src.entities.carrot_seed import CarrotSeed

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

        self.inventory = Inventory()
        self.inventory.add_item(CarrotSeed(10))
        self.inv_int = InventoryInterface(self.inventory)

        # Rostliny
        self.plants = []
        self.plants.append(Carrot((6, 6)))
        self.plants.append(Wheat((6, 7)))

        self.tilemap.add_plant(self.plants[0], (6, 6))
        self.tilemap.add_plant(self.plants[1], (6, 7))

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
            self.inv_int.handle_event(event)
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
            if self.player.energy >= self.player.get_required_energy_for_harvest():  # nepovinně
                self.player.harvest()
                self.tilemap.harvest_plant(tile_pos)
                print("Harvested plant")
            else:
                print("Nedostatek energie na sklizeň.")

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = self.player.handle_input(keys)
        self.player.move(dx, dy, self.obstacles)
        if self.player.interacting:
            plant_loc = (self.player.rect.centerx, self.player.rect.bottom)
            self.harvest_plant(plant_loc)
        
        for plant in self.plants:
            plant.update()

    def draw(self):
        self.tilemap.render(self.screen)
        for plant in self.plants:
            plant.render(self.screen)

        self.player.render(self.screen)

        self.inv_int.render(self.screen)

        # Pauzová zpráva
        if self.paused:
            paused_msg = self.font.render("PAUZA", True, (117, 55, 19))
            msg_rect = paused_msg.get_rect(center=(self.screen_width // 2, 40))
            self.screen.blit(paused_msg, msg_rect)

        # Lišta
        self.rim.draw(self.screen)
