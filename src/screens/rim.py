import pygame
import os

class Rim:
    def __init__(self, screen_width, screen_height, font, player):
        self.height = 60
        self.width = screen_width
        self.y = screen_height - self.height
        self.font = font
        self.player = player

        # Cesta k ikonám
        asset_path = os.path.join(os.path.dirname(__file__), "..", "assets", "tiles")
        load_icon = lambda name: pygame.transform.scale(
            pygame.image.load(os.path.join(asset_path, name)).convert_alpha(), (32, 32)
        )

        # Ikony
        self.pause_icon = load_icon("pause.png")
        self.quit_icon = load_icon("quit.png")
        self.sleep_icon = load_icon("sleep.png")
        self.eat_icon = load_icon("eat.png")

        # Umístění ikon
        bottom = screen_height - 10
        self.pause_button = self.pause_icon.get_rect(bottomright=(screen_width - 10, bottom))
        self.quit_button = self.quit_icon.get_rect(bottomright=(screen_width - 50, bottom))
        self.sleep_button = self.sleep_icon.get_rect(bottomright=(screen_width - 90, bottom))
        self.eat_button = self.eat_icon.get_rect(bottomright=(screen_width - 130, bottom))

    def draw(self, screen):
        background_color = (220, 200, 120)
        border_color = (160, 140, 80)
        text_color = (60, 40, 20)

        # Lišta
        pygame.draw.rect(screen, border_color, (0, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, background_color, (2, self.y + 2, self.width - 4, self.height - 4), border_radius=8)

        # Statistika
        info_text = f"fitness: {self.player.fitness}   EXP: {self.player.exp}/100   Energy: {int(self.player.energy)}"
        info = self.font.render(info_text, True, text_color)
        screen.blit(info, (20, self.y + 10))

        # Energie lišta
        energy_bar_x = 20
        energy_bar_y = self.y + 35
        energy_bar_width = 200
        energy_bar_height = 15
        energy_percent = self.player.energy / 100
        pygame.draw.rect(screen, (100, 100, 100), (energy_bar_x, energy_bar_y, energy_bar_width, energy_bar_height))
        pygame.draw.rect(screen, (50, 205, 50), (energy_bar_x, energy_bar_y, energy_bar_width * energy_percent, energy_bar_height))
        pygame.draw.rect(screen, border_color, (energy_bar_x, energy_bar_y, energy_bar_width, energy_bar_height), 2)

        # Ikony
        screen.blit(self.pause_icon, self.pause_button)
        screen.blit(self.quit_icon, self.quit_button)
        screen.blit(self.sleep_icon, self.sleep_button)
        screen.blit(self.eat_icon, self.eat_button)

    def handle_click(self, pos):
        if self.pause_button.collidepoint(pos):
            return "pause"
        if self.quit_button.collidepoint(pos):
            return "quit"
        if self.sleep_button.collidepoint(pos):
            return "sleep"
        if self.eat_button.collidepoint(pos):
            return "eat"
        return None

    def get_rect(self):
        return pygame.Rect(0, self.y, self.width, self.height)
