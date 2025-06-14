import pygame

class Player:
    def __init__(self, position_x, position_y, width, height, speed, screen_width, screen_height):
        self.image = pygame.image.load("src/assets/sprites/player/farmer_idle.png").convert_alpha()
        self.rect = pygame.Rect(position_x, position_y, width, height)
        self.speed = speed
        self.exp = 0
        self.level = 1
        self.screen_width = screen_width
        self.screen_height = screen_height

    def handle_input(self, keys):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
        return dx, dy

    def move(self, dx, dy, obstacles):
        if dx == 0 and dy == 0:
            return

        next_position = self.rect.move(dx, dy)

        # Kontrola okrajů obrazovky
        if (next_position.left < 0 or
            next_position.right > self.screen_width or
            next_position.top < 0 or
            next_position.bottom > self.screen_height):
            return  # Není pohyb = žádné expy

        # Kontrola překážek
        for obstacle in obstacles:
            if next_position.colliderect(obstacle):
                return  # Není pohyb = žádné expy

        # Povolený pohyb
        self.rect = next_position

        # Přidání expů
        self.exp += 1
        if self.exp >= 100:
            self.exp = 0
            self.level += 1

    def render(self, surface):
        surface.blit(self.image, self.rect.topleft)
