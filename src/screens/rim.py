import pygame
import os

class Rim:
    def __init__(self, screen_width, screen_height, font, player):
        self.height = 80
        self.width = screen_width
        self.y = screen_height - self.height
        self.font = pygame.font.SysFont("Courier New", 20)  # Nové písmo pro všechny texty
        self.player = player

        # Cesta k ikonám
        asset_path = os.path.join(os.path.dirname(__file__), "..", "assets", "tiles")
        load_icon = lambda name: pygame.transform.scale(
            pygame.image.load(os.path.join(asset_path, name)).convert_alpha(), (32, 32)
        )

        self.pause_icon = load_icon("pause.png")
        self.quit_icon = load_icon("quit.png")
        self.sleep_icon = load_icon("sleep.png")
        self.eat_icon = load_icon("eat.png")

        bottom = screen_height - 10
        self.quit_button = self.quit_icon.get_rect(bottomright=(screen_width - 10, bottom))
        self.pause_button = self.pause_icon.get_rect(bottomright=(screen_width - 50, bottom))
        self.sleep_button = self.sleep_icon.get_rect(bottomright=(screen_width - 90, bottom))
        self.eat_button = self.eat_icon.get_rect(bottomright=(screen_width - 130, bottom))

    def draw_bar(self, screen, label, value, max_value, x, y, width, height, fill_color, border_color, text_color):
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height))
        pygame.draw.rect(screen, fill_color, (x, y, width * (value / max_value), height))
        pygame.draw.rect(screen, border_color, (x, y, width, height), 2)

        value_text = f"{label}: {int(value)}/{int(max_value)}"
        text_surface = self.font.render(value_text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

    def get_energy_color(self):
        if self.player.energy > 60:
            return (50, 205, 50)
        elif self.player.energy > 30:
            return (255, 165, 0)
        else:
            return (220, 20, 60)

    def draw_tooltip(self, screen, text, button_rect):
        # Pouze čistý text bez pozadí a bez rámečku
        tooltip = self.font.render(text, True, (0, 0, 0))
        tooltip_rect = tooltip.get_rect(midbottom=(button_rect.centerx, button_rect.top - 4))
        screen.blit(tooltip, tooltip_rect)

    def draw(self, screen):
        background_color = (220, 200, 120)
        border_color = (160, 140, 80)
        text_color = (0, 0, 0)

        pygame.draw.rect(screen, border_color, (0, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, background_color, (2, self.y + 2, self.width - 4, self.height - 4), border_radius=8)

        bar_x = 20
        bar_width = 240
        bar_height = 30
        fitness_y = self.y + 8
        energy_y = self.y + 42

        self.draw_bar(screen, "Fitness", self.player.fitness, 100, bar_x, fitness_y, bar_width, bar_height,
                      (30, 144, 255), border_color, text_color)
        self.draw_bar(screen, "Energy", self.player.energy, 100, bar_x, energy_y, bar_width, bar_height,
                      self.get_energy_color(), border_color, text_color)

        screen.blit(self.pause_icon, self.pause_button)
        screen.blit(self.quit_icon, self.quit_button)
        screen.blit(self.sleep_icon, self.sleep_button)
        screen.blit(self.eat_icon, self.eat_button)

        mouse_pos = pygame.mouse.get_pos()
        if self.pause_button.collidepoint(mouse_pos):
            self.draw_tooltip(screen, "Pause", self.pause_button)
        elif self.quit_button.collidepoint(mouse_pos):
            self.draw_tooltip(screen, "Quit", self.quit_button)
        elif self.sleep_button.collidepoint(mouse_pos):
            self.draw_tooltip(screen, "Sleep", self.sleep_button)
        elif self.eat_button.collidepoint(mouse_pos):
            self.draw_tooltip(screen, f"Eat ({self.player.food})", self.eat_button)

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
