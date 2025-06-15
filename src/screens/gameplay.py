import pygame
import os
import random
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
from src.engine.audio_manager import AudioManager

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.day_cycle = DayCycle(day_length_seconds=120)
        self.running = True
        self.paused = False
        self.debug_mode = False
        self.font = pygame.font.SysFont("Arial", 24)
        self.prompt_font = pygame.font.SysFont("Arial", 18)
        self.show_sleep_prompt = False
        self.show_eat_prompt = False

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.assets = AssetManager()
        self.tilemap = Tilemap(self.assets)
        self.player = Player(100, 100, 40, 40, 5, self.screen_width, self.screen_height, self.day_cycle)

        # Lišta dole – s day_cycle
        self.rim = Rim(self.screen_width, self.screen_height, self.font, self.player, self.day_cycle)
        self.obstacles = [self.rim.get_rect()]

        self.inventory = Inventory(self.assets)
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

        # Audio
        audio_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "soundtrack-audio")
        self.audio_manager = AudioManager(audio_path)
        self.audio_manager.play()

        # Volume Icons
        self.volume_icons = {
            "high": pygame.image.load(os.path.join("src", "assets", "sounds", "sound-button-icons", "volume-2.png")).convert_alpha(),
            "low": pygame.image.load(os.path.join("src", "assets", "sounds", "sound-button-icons", "volume-1.png")).convert_alpha(),
            "muted": pygame.image.load(os.path.join("src", "assets", "sounds", "sound-button-icons", "volume-x.png")).convert_alpha()
        }
        self.volume_button_rect = self.volume_icons["high"].get_rect(topleft=(10, 10))

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
                
                if self.volume_button_rect.collidepoint(event.pos):
                    self.audio_manager.cycle_volume()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    self.debug_mode = not self.debug_mode
                elif event.key == pygame.K_e:
                    if self.player.rect.colliderect(self.house.bed_interaction_rect):
                        self.player.sleep()
                    elif self.player.rect.colliderect(self.house.cauldron_interaction_rect):
                        self.player.eat()

    def harvest_plant(self, pos):
        tile_pos = self.tilemap.pixel_to_tile_pos(pos)
        plant = self.tilemap.get_plant(tile_pos)
        if plant and plant.ready_to_harvest():
            if self.player.energy >= self.player.get_required_energy_for_harvest():
                self.player.harvest()
                self.tilemap.harvest_plant(tile_pos)
                self.inventory.add_item(plant.get_item())
                amt = random.randint(1, 2)
                item = plant.associated_seed()
                item.amount = amt
                self.inventory.add_item(item)
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
        self.audio_manager.update()

        keys = pygame.key.get_pressed()
        dx, dy = self.player.handle_input(keys)
        self.player.is_moving = self.player.move(dx, dy, self.obstacles)

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

        # Check for proximity to bed and cauldron
        if self.player.rect.colliderect(self.house.bed_interaction_rect):
            self.show_sleep_prompt = True
        else:
            self.show_sleep_prompt = False

        if self.player.rect.colliderect(self.house.cauldron_interaction_rect):
            self.show_eat_prompt = True
        else:
            self.show_eat_prompt = False

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

        if self.show_sleep_prompt:
            text = self.prompt_font.render("Press E to sleep", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.player.rect.centerx, self.player.rect.top - 20))
            pygame.draw.rect(self.screen, (0, 0, 0, 150), text_rect.inflate(10, 5))
            self.screen.blit(text, text_rect)

        # Volume button
        volume_state = self.audio_manager.get_volume_state()
        icon = self.volume_icons[volume_state]
        
        # Vykreslení tlačítka s tlustším a zakulaceným okrajem
        border_rect = self.volume_button_rect.inflate(4, 4)
        pygame.draw.rect(self.screen, (255, 255, 255), border_rect, 2, border_radius=5)
        self.screen.blit(icon, self.volume_button_rect)
        
        if self.show_eat_prompt:
            text = self.prompt_font.render("Press E to eat", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.player.rect.centerx, self.player.rect.top - 20))
            pygame.draw.rect(self.screen, (0, 0, 0, 150), text_rect.inflate(10, 5))
            self.screen.blit(text, text_rect)
