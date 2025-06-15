import pygame

class MoneyIndicator:
    def __init__(self, inventory, offset=(0, 0)):
        self.inventory = inventory
        self.offset = offset  # Offset from the top-right corner of the indicator

    def render(self, surf, indicator_rect):
        # Get the icon and amount
        icon = self.inventory.money_icon
        money = self.inventory.money

        # Prepare icon and text
        icon_size = 28
        icon_surf = pygame.transform.smoothscale(icon, (icon_size, icon_size))
        font = pygame.font.SysFont("arial", 22, bold=True)
        money_text = font.render(str(money), True, (60, 40, 20))

        # Position: top-right of indicator_rect, with offset
        padding = 10
        x = indicator_rect.right + padding + self.offset[0]
        y = indicator_rect.top + padding + self.offset[1]

        # Draw icon and text (left-aligned)
        surf.blit(icon_surf, (x, y))
        surf.blit(money_text, (x + icon_size + 4, y + (icon_size - money_text.get_height()) // 2))