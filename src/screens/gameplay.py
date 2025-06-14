import pygame

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 24)

        # Herní stav
        self.gardener_pos = [100, 100]
        self.exp = 0
        self.level = 1

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        speed = 4
        if keys[pygame.K_LEFT]:
            self.gardener_pos[0] -= speed
        if keys[pygame.K_RIGHT]:
            self.gardener_pos[0] += speed
        if keys[pygame.K_UP]:
            self.gardener_pos[1] -= speed
        if keys[pygame.K_DOWN]:
            self.gardener_pos[1] += speed

    def update(self):
        # Získávání zkušeností pohybem (pro ukázku)
        self.exp += 1
        if self.exp >= 100:
            self.exp = 0
            self.level += 1

    def draw(self):
        self.screen.fill((34, 139, 34))  # zelená zahrada

        # Zahradník (čtverec)
        pygame.draw.rect(self.screen, (139, 69, 19), (*self.gardener_pos, 40, 40))

        # Info panel
        info = self.font.render(f"Level: {self.level}   EXP: {self.exp}/100", True, (255, 255, 255))
        self.screen.blit(info, (10, 10))
