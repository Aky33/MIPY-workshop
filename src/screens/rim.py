import pygame
import os

class Rim:
    def __init__(self, screen_width, screen_height, font, player, day_cycle):
        self.height = 80
        self.width = screen_width
        self.y = screen_height - self.height
        self.font = pygame.font.SysFont("Courier New", 22, bold=True)
        self.player = player
        self.day_cycle = day_cycle

        # Cesta k ikonám
        asset_path = os.path.join(os.path.dirname(__file__), "..", "assets", "tiles")
        load_icon = lambda name: pygame.transform.scale(
            pygame.image.load(os.path.join(asset_path, name)).convert_alpha(), (32, 32)
        )

        self.pause_icon = load_icon("pause.png")
        self.quit_icon = load_icon("quit.png")
        self.clock_icon = load_icon("clock.png")

        bottom = screen_height - 10
        self.pause_button = self.pause_icon.get_rect(bottomright=(screen_width - 10, bottom))
        self.quit_button = self.quit_icon.get_rect(bottomright=(screen_width - 50, bottom))

    def draw_bar(self, screen, label, value, max_value, x, y, width, height, fill_color, border_color, text_color):
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height))
        pygame.draw.rect(screen, fill_color, (x, y, width * (value / max_value), height))
        pygame.draw.rect(screen, border_color, (x, y, width, height), 2)

        value_text = f"{label}: {int(value)}/{int(max_value)}"
        text_surface = self.font.render(value_text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2 + 2)) # posun o 2px dolů
        screen.blit(text_surface, text_rect)

    def get_energy_color(self):
        if self.player.energy > 60:
            return (50, 205, 50)
        elif self.player.energy > 30:
            return (255, 165, 0)
        else:
            return (220, 20, 60)

    def draw_tooltip(self, screen, text, button_rect):
        tooltip = self.font.render(text, True, (0, 0, 0))
        bg_rect = tooltip.get_rect(midbottom=(button_rect.centerx, button_rect.top - 2))
        bg_rect.inflate_ip(6, 4)
        pygame.draw.rect(screen, (255, 255, 200), bg_rect)
        pygame.draw.rect(screen, (100, 100, 50), bg_rect, 1)
        screen.blit(tooltip, tooltip.get_rect(center=bg_rect.center))

    def draw(self, screen):
        background_color = (220, 200, 120)
        border_color = (160, 140, 80)
        text_color = (0, 0, 0)

        pygame.draw.rect(screen, border_color, (0, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, background_color, (2, self.y + 2, self.width - 4, self.height - 4), border_radius=8)

        # Statistiky
        bar_x = 20
        bar_width = 240
        bar_height = 30
        fitness_y = self.y + 8
        energy_y = self.y + 42

        self.draw_bar(screen, "Fitness", self.player.fitness, 100, bar_x, fitness_y, bar_width, bar_height,
                      (30, 144, 255), border_color, text_color)
        self.draw_bar(screen, "Energy", self.player.energy, 100, bar_x, energy_y, bar_width, bar_height,
                      self.get_energy_color(), border_color, text_color)

        # Ikony
        screen.blit(self.pause_icon, self.pause_button)
        screen.blit(self.quit_icon, self.quit_button)

        # Čas v pravém horním rohu spodní lišty
        time_str = self.day_cycle.get_time_string()  # např. "08:15"
        time_surface = self.font.render(time_str, True, text_color)
        
        # Pozice pro text času
        time_rect = time_surface.get_rect(topright=(self.width - 10, self.y + 10))
        
        # Pozice pro ikonu hodin (nalevo od textu)
        clock_icon_rect = self.clock_icon.get_rect(right=time_rect.left - 5, centery=time_rect.centery)
        
        screen.blit(time_surface, time_rect)
        screen.blit(self.clock_icon, clock_icon_rect)


    def handle_click(self, pos):
        if self.pause_button.collidepoint(pos):
            return "pause"
        if self.quit_button.collidepoint(pos):
            return "quit"
        return None

    def get_rect(self):
        return pygame.Rect(0, self.y, self.width, self.height)
