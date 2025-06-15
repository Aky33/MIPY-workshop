import pygame
from src.screens.inventory_visual import InventoryVisual
from src.entities.selected_item_indicator import SelectedItemIndicator
from src.entities.money_indicator import MoneyIndicator

class InventoryInterface:
    def __init__(self, inventory, grid_size=(5, 3), inv_pos=(180, 215), indicator_pos=(262, 405)):
        self.inventory = inventory
        self.visual = InventoryVisual(inventory, grid_size=grid_size, pos=inv_pos)
        self.indicator = SelectedItemIndicator(inventory, pos=indicator_pos)
        self.money_indicator = MoneyIndicator(inventory, (-10, 25))

    def render(self, surf):
        self.visual.render(surf)
        self.indicator.render(surf)
        # Draw money indicator at top right of the indicator
        self.money_indicator.render(surf, self.indicator.get_rect())

    def handle_event(self, event):
        # Handle opening inventory by clicking the indicator
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            indicator_rect = self.indicator.get_rect()
            if indicator_rect.collidepoint(event.pos):
                self.visual.visible = not self.visual.visible
                return  # Don't pass event to inventory if just toggled

        self.visual.handle_event(event)