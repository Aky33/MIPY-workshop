import pygame

class SelectedItemIndicator:
    def __init__(self, inventory, pos=(20, 20), bg_color=(240, 220, 160), border_color=(160, 140, 80)):
        self.inventory = inventory
        self.pos = pos
        self.bg_color = bg_color
        self.border_color = border_color
        self.base_height = 70
        self.base_width = 215
        self.icon_size = 40  # Adjust as needed
        self.vertical_padding = 10  # Vertical padding for text
        self._last_rect = pygame.Rect(self.pos[0], self.pos[1], self.base_width, self.base_height)

    def render(self, surf):
        item = self.inventory.get_item(self.inventory.selected)

        font = pygame.font.SysFont("Courier New", 18, bold=True)
        amount_font = pygame.font.SysFont("Courier New", 14, bold=True)

        rect = pygame.Rect(self.pos[0], self.pos[1], self.base_width, self.base_height)
        self._last_rect = rect
        pygame.draw.rect(surf, self.bg_color, rect, border_radius=10)
        pygame.draw.rect(surf, self.border_color, rect, width=3, border_radius=10)

        if item:
            # Prepare icon
            icon = item.icon_asset
            icon_rect = icon.get_rect()
            icon_rect.width = self.icon_size
            icon_rect.height = self.icon_size

            # Prepare text
            max_text_width = self.base_width - (10 + self.icon_size + 12 + 20)
            name = item.name
            name_text = font.render(name, True, (60, 40, 20))
            # Truncate name if too wide
            while name_text.get_width() > max_text_width and len(name) > 0:
                name = name[:-1]
                name_text = font.render(name + "...", True, (60, 40, 20))
            if name != item.name:
                name += "..."
                name_text = font.render(name, True, (60, 40, 20))

            amount_text = amount_font.render(f"x{item.amount}", True, (60, 40, 20))

            # Draw icon
            icon_y = self.pos[1] + (self.base_height - self.icon_size) // 2
            surf.blit(pygame.transform.smoothscale(icon, (self.icon_size, self.icon_size)), (self.pos[0] + 10, icon_y))

            # Draw name and amount
            text_x = self.pos[0] + 10 + self.icon_size + 12
            surf.blit(name_text, (text_x, self.pos[1] + self.vertical_padding))
            surf.blit(amount_text, (text_x, self.pos[1] + self.vertical_padding + name_text.get_height() + 8))
        else:
            font = pygame.font.SysFont("Courier New", 18, bold=True)
            text = font.render("No item selected", True, (100, 80, 40))
            surf.blit(text, (self.pos[0] + 16, self.pos[1] + (self.base_height - text.get_height()) // 2))

    def get_rect(self):
        return self._last_rect