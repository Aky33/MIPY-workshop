import pygame

class InventoryVisual:
    def __init__(self, inventory, grid_size=(5, 3), cell_size=48, margin=12, pos=(50, 50)):
        self.inventory = inventory
        self.bg_color = (220, 200, 120)
        self.border_color = (160, 140, 80)
        self.cell_size = cell_size
        self.grid_size = grid_size  # (cols, rows)
        self.margin = margin
        self.pos = pos  # Top-left position of inventory

    def draw_background(self, surf):
        width = self.grid_size[0] * self.cell_size + self.margin * 2
        height = self.grid_size[1] * self.cell_size + self.margin * 2
        rect = pygame.Rect(self.pos[0], self.pos[1], width, height)
        pygame.draw.rect(surf, self.bg_color, rect, border_radius=12)
        pygame.draw.rect(surf, self.border_color, rect, width=4, border_radius=12)

    def draw_grid(self, surf):
        items = self.inventory.list_items()
        cols, rows = self.grid_size
        for i in range(cols * rows):
            x = i % cols
            y = i // cols
            cell_x = self.pos[0] + self.margin + x * self.cell_size
            cell_y = self.pos[1] + self.margin + y * self.cell_size
            cell_rect = pygame.Rect(cell_x, cell_y, self.cell_size, self.cell_size)
            # Draw cell background
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

    def draw(self, surf):
        self.draw_background(surf)
        self.draw_grid(surf)
