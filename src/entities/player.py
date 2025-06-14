import pygame

class Player:
    def __init__(self, position_x, position_y, width, height):
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.speed = 4
        self.exp = 0
        self.level = 1

    def handle_movement(self, keys):
        movement = False

        if keys[pygame.K_LEFT]:
            self.position_x -= self.speed
            movement = True
        if keys[pygame.K_RIGHT]:
            self.position_x += self.speed
            movement = True
        if keys[pygame.K_UP]:
            self.position_y -= self.speed
            movement = True
        if keys[pygame.K_DOWN]:
            self.position_y += self.speed
            movement = True

        if movement:
            self.position_x = max(0, min(self.position_x, pygame.display.get_surface().get_width() - self.width))
            self.position_y = max(0, min(self.position_y, pygame.display.get_surface().get_height() - self.height))

            self.exp += 1
            if self.exp >= 100:
                self.exp = 0
                self.level += 1
