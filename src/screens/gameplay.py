import pygame
import os
from src.entities.player import Player
from src.engine.asset_manager import AssetManager
from src.engine.tilemap import Tilemap
from src.entities.plant import Plant
from src.entities.carrot import Carrot
from src.entities.wheat import Wheat
from src.entities.house import House
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
        self.debug_mode = False
        self.font = pygame.font.SysFont("Arial", 24)
        self.prompt_font = pygame.font.SysFont("Arial", 18)
        self.show_sleep_prompt = False
        self.show_eat_prompt = False

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

        # Dům
        self.house = House((self.screen_width - 210, 0))
        self.obstacles.extend(self.house.get_obstacles())

        # Načtení pixelové pauza ikony
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
                print("Harvested plant")
            else:
                print("Nedostatek energie na sklizeň.")
    
    def plant_seed(self, pos):
        tile_pos = self.tilemap.pixel_to_tile_pos(pos)
        seed = self.inventory.selected
        if self.tilemap.get_plant(tile_pos) != False:
            print("Cant plant, farmland already occupied")
        self.tilemap.add_plant(seed.associated_plant(), tile_pos)

    def can_plant(self):
        return self.inventory.selected != None and self.inventory.selected.plantable == True


    def update(self):
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

        # Check for proximity to bed
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
                # Draw obstacles that are not part of the house (e.g., the rim)
                if obstacle not in self.house.get_obstacles():
                     pygame.draw.rect(self.screen, (128, 0, 128, 150), obstacle)

        # Pauzová zpráva jako obrázek
        if self.paused:
            self.screen.blit(self.pause_image, self.pause_rect)

        # Lišta
        self.rim.draw(self.screen)
        self.inv_int.render(self.screen)

        if self.show_sleep_prompt:
            text = self.prompt_font.render("Press E to sleep", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.player.rect.centerx, self.player.rect.top - 20))
            pygame.draw.rect(self.screen, (0, 0, 0, 150), text_rect.inflate(10, 5))
            self.screen.blit(text, text_rect)
        
        if self.show_eat_prompt:
            text = self.prompt_font.render("Press E to eat", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.player.rect.centerx, self.player.rect.top - 20))
            pygame.draw.rect(self.screen, (0, 0, 0, 150), text_rect.inflate(10, 5))
            self.screen.blit(text, text_rect)
