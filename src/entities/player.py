import pygame

class Player:
    def __init__(self, position_x, position_y, width, height, speed):
        self.rect = pygame.Rect(position_x, position_y, width, height)
        self.speed = speed
        self.exp = 0
        self.level = 1

    def handle_input(self, keys):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

        return dx, dy
    
    def move(self, dx, dy, obstacles):
        #kontrola zda jsme se vůbec pohnuli
        if dx == 0 and dy == 0:
            return

        next_position = self.rect.move(dx, dy)

        collision = False
        for obstacle in obstacles:
            if next_position.colliderect(obstacle):
                collision = True
                break

        if not collision:
            self.rect = next_position

        #epxy, hlavně jako ukázka
        self.exp += 1
        if self.exp >= 100:
            self.exp = 0
            self.level += 1

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), self.rect)
