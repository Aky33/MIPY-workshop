import pygame
import os
from src.entities.player import Player
from src.engine.asset_manager import AssetManager
from src.engine.tilemap import Tilemap
from src.entities.carrot import Carrot
from src.entities.wheat import Wheat
from src.entities.house import House
from src.screens.rim import Rim
from src.gameplay.inventory import Inventory
from src.screens.inventory_interface import InventoryInterface
from src.entities.carrot_seed import CarrotSeed
from src.engine.day_cycle import DayCycle

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.day_cycle = DayCycle(day_length_seconds=120)
        self.running = True
        self.paused = False
        self.debug_mode = False
        self.font = pygame.font.SysFont("Arial", 24)

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.assets = AssetManager()
        self.tilemap = Tilemap(self.assets)
        self.player = Player(100, 100, 40, 40, 5, self.screen_width, self.screen_height)

        # Lišta dole – s day_cycle
        self.rim = Rim(self.screen_width, self.screen_height, self.font, self.player, self.day_cycle)
        self.obstacles = [self.rim.get_rect()]

        self.inventory = Inventory()
        self.inventory.add_item(CarrotSeed(10))
        self.inv_int = InventoryInterface(self.inventory)

        # Rostliny
        self.plants = []
        self.plants.append(Carrot((6, 6)))
        self.plants.append(Wheat((6, 7)))
        self.tilemap.add_plant(self.plants[0], (6, 6))
        self.tilemap.add_plant(self.plants[1], (6, 7))

        # Dům
        self.house = House((self.screen_width - 210, 0))
        self.obstacles.extend(self.house.get_obstacles())

        # Pauza obrázek
        pause_icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "tiles", "pause_icon_pixel.png")
        self.pause_image = pygame.image.load(pause_icon_path).convert_alpha()
        self.pause_image = pygame.transform.scale(self.pause_image, (200, 200))
        self.pause_rect = self.pause_image.get_rect(center=(self.screen_width // 2, 40))

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    self.debug_mode = not self.debug_mode
                elif event.key == pygame.K_f:
                    if self.player.rect.colliderect(self.house.bed_rect):
                        self.player.sleep()
                    elif self.player.rect.colliderect(self.house.cauldron_rect):
                        self.player.eat()

    def harvest_plant(self, pos):
        tile_pos = self.tilemap.pixel_to_tile_pos(pos)
        plant = self.tilemap.get_plant(tile_pos)
        if plant and plant.ready_to_harvest():
            if self.player.energy >= self.player.get_required_energy_for_harvest():
                self.player.harvest()
                self.tilemap.harvest_plant(tile_pos)
                self.inventory.add_item(plant.get_item())
                print("Harvested plant")
            else:
                print("Nedostatek energie na sklizeň.")

    def plant_seed(self, pos):
        tile_pos = self.tilemap.pixel_to_tile_pos(pos)
        seed = self.inventory.get_item(self.inventory.selected)
        if self.tilemap.get_plant(tile_pos) or not self.tilemap.is_farmland(tile_pos):
            print("Cant plant, invalid location or already occupied")
            return
        plant = seed.associated_plant()
        self.tilemap.add_plant(plant, tile_pos)
        self.plants.append(plant)
        self.inventory.remove_item(seed.id)
        print(f"Planted {seed.name}")

    def can_plant(self):
        item = self.inventory.get_item(self.inventory.selected)
        return item is not None and item.plantable

    def update(self):
        dt = self.clock.get_time() / 1000  # delta time in seconds
        self.day_cycle.update(dt)

        keys = pygame.key.get_pressed()
        dx, dy = self.player.handle_input(keys)
        self.player.move(dx, dy, self.obstacles)

        if self.player.interacting:
            plant_loc = (self.player.rect.centerx, self.player.rect.bottom)
            self.harvest_plant(plant_loc)
            if self.can_plant():
                self.plant_seed(plant_loc)

        for plant in self.plants:
            plant.update()

        # Snížení energie v noci
        if self.day_cycle.time_of_day == "night":
            self.player.energy = max(0, self.player.energy - 0.05)

    def draw(self):
        self.tilemap.render(self.screen)
        self.house.render(self.screen, self.debug_mode)

        for plant in self.plants:
            plant.render(self.screen)

        self.player.render(self.screen, self.debug_mode)

        if self.debug_mode:
            for obstacle in self.obstacles:
                if obstacle not in self.house.get_obstacles():
                    pygame.draw.rect(self.screen, (128, 0, 128, 150), obstacle)

        if self.paused:
            self.screen.blit(self.pause_image, self.pause_rect)

        # Denní doba overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill(self.day_cycle.get_overlay_color())
        self.screen.blit(overlay, (0, 0))

        # Spodní lišta a inventář
        self.rim.draw(self.screen)
        self.inv_int.render(self.screen)
