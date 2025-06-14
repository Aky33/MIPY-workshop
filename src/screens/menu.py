import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 36)

        self.start_button_rect = pygame.Rect(220, 190, 200, 60)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    self.running = False  # Ukonči menu -> začne hra

    def draw(self):
        self.screen.fill((30, 30, 30))  # tmavé pozadí
        pygame.draw.rect(self.screen, (70, 130, 180), self.start_button_rect)

        text = self.font.render("Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(text, text_rect)
