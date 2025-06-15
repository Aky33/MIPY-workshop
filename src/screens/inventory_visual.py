import pygame

class InventoryVisual:
    def __init__(self, inventory, grid_size=(5, 3), cell_size=52, margin=12, pos=(50, 50), cell_padding=6):
        self.inventory = inventory
        self.bg_color = (220, 200, 120)
        self.border_color = (160, 140, 80)
        self.selected_color = (255, 220, 80)
        self.cell_size = cell_size
        self.grid_size = grid_size  # (cols, rows)
        self.margin = margin
        self.pos = pos  # Top-left position of inventory
        self.cell_padding = cell_padding
        self.visible = False  # Inventory is closed by default
        self._sell_button_rect = None  # Store sell button rect for click detection

    def draw_background(self, surf):
        width = self.grid_size[0] * self.cell_size + self.margin * 2
        height = self.grid_size[1] * self.cell_size + self.margin * 2
        rect = pygame.Rect(self.pos[0], self.pos[1], width, height)
        pygame.draw.rect(surf, self.bg_color, rect, border_radius=12)
        pygame.draw.rect(surf, self.border_color, rect, width=4, border_radius=12)

    def draw_grid(self, surf):
        items = self.inventory.list_items()
        cols, rows = self.grid_size
        selected_index = None
        for i in range(cols * rows):
            x = i % cols
            y = i // cols
            cell_x = self.pos[0] + self.margin + x * self.cell_size + self.cell_padding // 2
            cell_y = self.pos[1] + self.margin + y * self.cell_size + self.cell_padding // 2
            cell_rect = pygame.Rect(
                cell_x,
                cell_y,
                self.cell_size - self.cell_padding,
                self.cell_size - self.cell_padding
            )
            # Highlight if selected
            if i < len(items) and self.inventory.selected == items[i].id:
                pygame.draw.rect(surf, self.selected_color, cell_rect, border_radius=8)
                pygame.draw.rect(surf, (255, 180, 40), cell_rect, width=3, border_radius=8)
                selected_index = i
                selected_rect = cell_rect
            else:
                pygame.draw.rect(surf, (245, 230, 170), cell_rect, border_radius=8)
                pygame.draw.rect(surf, self.border_color, cell_rect, width=2, border_radius=8)
            # Draw item if present
            if i < len(items):
                item = items[i]
                icon = item.icon_asset
                # Center icon in cell
                icon_rect = icon.get_rect(center=cell_rect.center)
                surf.blit(icon, icon_rect)
                # Draw amount if more than 1
                if item.amount > 1:
                    font = pygame.font.SysFont("arial", 16, bold=True)
                    text = font.render(str(item.amount), True, (60, 40, 20))
                    text_rect = text.get_rect(bottomright=(cell_rect.right - 6, cell_rect.bottom - 4))
                    # Draw text outline for readability
                    outline = font.render(str(item.amount), True, (255, 255, 200))
                    surf.blit(outline, text_rect.move(1, 1))
                    surf.blit(text, text_rect)

        # Draw sell button if selected item is sellable
        self._sell_button_rect = None
        selected_item = self.inventory.get_item(self.inventory.selected)
        if selected_item and selected_item.price > 0 and selected_index is not None:
            # Place the button just below the selected cell
            font = pygame.font.SysFont("arial", 18, bold=True)
            icon = self.inventory.money_icon
            icon_size = 28
            icon_surf = pygame.transform.smoothscale(icon, (icon_size, icon_size))
            price_text = font.render(f"Sell ({selected_item.price})", True, (80, 60, 20))

            # Decrease spacing between icon and text
            spacing = 2
            total_width = icon_size + spacing + price_text.get_width()
            btn_width = total_width + 18  # 9px padding on each side
            btn_height = max(icon_size, price_text.get_height()) + 12  # 6px padding top/bottom

            btn_x = selected_rect.centerx - btn_width // 2
            btn_y = selected_rect.bottom + 8
            self._sell_button_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)

            # Draw background and border
            pygame.draw.rect(surf, (255, 230, 120), self._sell_button_rect, border_radius=8)
            pygame.draw.rect(surf, (180, 140, 40), self._sell_button_rect, width=2, border_radius=8)

            # Center icon and text vertically
            btn_center = self._sell_button_rect.center
            icon_x = btn_x + 9
            icon_y = btn_center[1] - icon_size // 2
            text_x = icon_x + icon_size + spacing
            text_y = btn_center[1] - price_text.get_height() // 2

            surf.blit(icon_surf, (icon_x, icon_y))
            surf.blit(price_text, (text_x, text_y))

    def render(self, surf):
        if self.visible:
            self.draw_background(surf)
            self.draw_grid(surf)

    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            # Check sell button first
            if self._sell_button_rect and self._sell_button_rect.collidepoint(mouse_x, mouse_y):
                selected_item = self.inventory.get_item(self.inventory.selected)
                if selected_item and selected_item.price > 0:
                    # Sell one item
                    self.inventory.money += selected_item.price
                    self.inventory.remove_item(selected_item.id, 1)
                    # If no more, deselect
                    if not self.inventory.get_item(selected_item.id):
                        self.inventory.selected = None
                return
            # Otherwise, check grid
            cols, rows = self.grid_size
            for i in range(cols * rows):
                x = i % cols
                y = i // cols
                cell_x = self.pos[0] + self.margin + x * self.cell_size + self.cell_padding // 2
                cell_y = self.pos[1] + self.margin + y * self.cell_size + self.cell_padding // 2
                cell_rect = pygame.Rect(
                    cell_x,
                    cell_y,
                    self.cell_size - self.cell_padding,
                    self.cell_size - self.cell_padding
                )
                if cell_rect.collidepoint(mouse_x, mouse_y):
                    items = self.inventory.list_items()
                    if i < len(items):
                        self.inventory.selected = items[i].id
                    else:
                        self.inventory.selected = None
                    break
