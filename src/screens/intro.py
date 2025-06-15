import pygame

class Intro:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Georgia", 60, bold=True)

        self.title = "GARDENATOR"

    def run(self):
        start_time = pygame.time.get_ticks()
        displayed_chars = 0
        delay_per_char = 100  # v milisekundách (100 ms = 10 znaků za sekundu)

        running = True
        while running:
            self.screen.fill((144, 238, 144))

            # Kolik znaků zobrazit podle uplynulého času
            now = pygame.time.get_ticks()
            displayed_chars = min(len(self.title), (now - start_time) // delay_per_char)

            # Vykreslení nadpisu
            current_text = self.title[:displayed_chars]
            text_surface = self.font.render(current_text, True, (34, 85, 34))
            self.screen.blit(text_surface, (100, 200))

            # Pokud se nadpis celý vykreslil, zobraz další instrukci
            if displayed_chars == len(self.title):
                running = False

            pygame.display.flip()
            self.clock.tick(60)