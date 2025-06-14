import pygame
import random
import os
from src.screens.gameplay import Gameplay


class FlyingSprite:
    def __init__(self, image, screen_width, screen_height, is_bee=False):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -10)
        self.speed_y = random.uniform(0.5, 1.5)
        self.speed_x = random.uniform(-0.5, 0.5) if is_bee else 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_bee = is_bee

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Pokud vyletí mimo obrazovku, resetuj
        if self.rect.top > self.screen_height or self.rect.left > self.screen_width or self.rect.right < 0:
            self.rect.x = random.randint(0, self.screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -10)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_title = pygame.font.SysFont("Georgia", 60, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 32)

        self.start_button_rect = pygame.Rect(220, 250, 200, 60)

        self.bg_color = (144, 238, 144)
        self.button_color = (60, 179, 113)
        self.button_hover = (46, 139, 87)
        self.text_color = (255, 255, 255)

        self.title_text = "Garden RPG"

        # Načtení obrázků
        asset_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        leaf_img_path = os.path.join(asset_path, "leaf.png")
        bee_img_path = os.path.join(asset_path, "bee.png")

        self.leaf_img = pygame.image.load(leaf_img_path).convert_alpha()
        self.bee_img = pygame.image.load(bee_img_path).convert_alpha()

        # Animace – listy a včely
        self.falling_leaves = [FlyingSprite(self.leaf_img, screen.get_width(), screen.get_height()) for _ in range(20)]
        self.bees = [FlyingSprite(self.bee_img, screen.get_width(), screen.get_height(), is_bee=True) for _ in range(5)]

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
        for leaf in self.falling_leaves:
            leaf.update()
        for bee in self.bees:
            bee.update()

    def draw(self):
        self.screen.fill(self.bg_color)

        for leaf in self.falling_leaves:
            leaf.draw(self.screen)

        for bee in self.bees:
            bee.draw(self.screen)

        # Nadpis
        title = self.font_title.render(self.title_text, True, (34, 85, 34))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title, title_rect)

        # Tlačítko START
        mouse_pos = pygame.mouse.get_pos()
        color = self.button_hover if self.start_button_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, color, self.start_button_rect, border_radius=12)

        text = self.font_button.render("Start", True, self.text_color)
        text_rect = text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(text, text_rect)
