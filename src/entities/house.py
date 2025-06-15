import pygame
import os

class House:
    def __init__(self, position):
        # Cesty k obrázkům
        base_path = os.path.join("src", "assets", "tiles", "house")
        interior_path = os.path.join(base_path, "house_interior.png")
        bed_path = os.path.join(base_path, "bed.png")
        cauldron_path = os.path.join(base_path, "cauldron.png")

        # Načtení obrázků
        self.interior_image = pygame.image.load(interior_path).convert_alpha()
        self.bed_image = pygame.image.load(bed_path).convert_alpha()
        self.cauldron_image = pygame.image.load(cauldron_path).convert_alpha()

        # Pozice domu a objektů
        self.rect = self.interior_image.get_rect(topleft=position)
        self.bed_rect = self.bed_image.get_rect(center=(self.rect.centerx - 80, self.rect.centery + 30))
        self.bed_rect.inflate_ip(-16, -28) # Zmenseni kolizniho boxu
        self.bed_interaction_rect = self.bed_rect.inflate(20, 20) # Vytvoření většího boxu pro interakci
        self.cauldron_rect = self.cauldron_image.get_rect(center=(self.rect.centerx - 67, self.rect.centery - 60))
        self.cauldron_interaction_rect = self.cauldron_rect.inflate(20, 20) # Vytvoření většího boxu pro interakci

        # Definovani sten pro kolize
        top_thickness = 25
        bottom_thickness = 15
        side_thickness = 15
        door_width = 85

        # Vypocet pro spodni stenu
        left_wall_width = (self.rect.width - door_width) / 2
        right_wall_start = self.rect.left + left_wall_width + door_width
        right_wall_width = self.rect.width - right_wall_start + self.rect.left

        self.walls = [
            # Horni stena
            pygame.Rect(self.rect.left, self.rect.top, self.rect.width, top_thickness),
            # Leva stena
            pygame.Rect(self.rect.left, self.rect.top, side_thickness, self.rect.height),
            # Prava stena
            pygame.Rect(self.rect.right - side_thickness, self.rect.top, side_thickness, self.rect.height),
            # Spodni stena (s mezerou pro dvere)
            pygame.Rect(self.rect.left, self.rect.bottom - bottom_thickness, left_wall_width, bottom_thickness),
            pygame.Rect(right_wall_start, self.rect.bottom - bottom_thickness, right_wall_width, bottom_thickness),
        ]

    def get_obstacles(self):
        return self.walls + [self.bed_rect, self.cauldron_rect]

    def render(self, surface, debug=False):
        surface.blit(self.interior_image, self.rect)
        surface.blit(self.bed_image, self.bed_rect.topleft)
        surface.blit(self.cauldron_image, self.cauldron_rect.topleft)

        if debug:
            for wall in self.walls:
                pygame.draw.rect(surface, (255, 0, 0, 150), wall)
            pygame.draw.rect(surface, (0, 255, 0, 150), self.bed_rect)
            pygame.draw.rect(surface, (255, 255, 0, 100), self.bed_interaction_rect) # Vykreslení interakčního boxu v debug modu
            pygame.draw.rect(surface, (0, 0, 255, 150), self.cauldron_rect)
            pygame.draw.rect(surface, (255, 165, 0, 100), self.cauldron_interaction_rect) # Vykreslení interakčního boxu v debug modu