import pygame
import random
import os
from src.screens.gameplay import Gameplay


class FlyingSprite:
    def __init__(self, image, screen_width, screen_height):
        self.image = image
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.speed_x = random.uniform(-1.5, -0.3)
        self.speed_y = random.uniform(-1.0, 1.0)
        self.dir_change_timer = random.randint(30, 90)

    def update(self):
        self.dir_change_timer -= 1
        if self.dir_change_timer <= 0:
            self.speed_x = random.uniform(-1.5, -0.3)
            self.speed_y = random.uniform(-1.0, 1.0)
            self.dir_change_timer = random.randint(30, 90)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if (self.rect.right < 0 or
            self.rect.bottom < 0 or self.rect.top > self.screen_height):
            self.rect.x = self.screen_width
            self.rect.y = random.randint(0, self.screen_height - self.rect.height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # Cesty
        tiles_path = os.path.join(os.path.dirname(__file__), "..", "assets", "tiles")
        bee_img_path = os.path.join(tiles_path, "bee.png")
        start_icon_path = os.path.join(tiles_path, "start_icon.png")
        background_path = os.path.join(tiles_path, "menu_background.png")

        # Načtení obrázků
        self.bee_img = pygame.transform.scale(
            pygame.image.load(bee_img_path).convert_alpha(), (32, 32)
        )
        self.start_icon = pygame.transform.scale(
            pygame.image.load(start_icon_path).convert_alpha(), (200, 200)
        )
        self.background = pygame.image.load(background_path).convert()
        self.background = pygame.transform.scale(self.background, screen.get_size())

        self.start_button_rect = self.start_icon.get_rect(center=(self.screen.get_width() // 2, 260))

        # Včely
        self.bees = [
            FlyingSprite(self.bee_img, screen.get_width(), screen.get_height())
            for _ in range(3)
        ]

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    self.running = False
                    gameplay = Gameplay(self.screen)
                    gameplay.run()

    def update(self):
        for bee in self.bees:
            bee.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for bee in self.bees:
            bee.draw(self.screen)

        # Zvýraznění ikony při přejetí
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.start_button_rect.collidepoint(mouse_pos)
        icon = self.start_icon.copy()
        icon.set_alpha(255 if hovered else 200)
        self.screen.blit(icon, self.start_button_rect)
