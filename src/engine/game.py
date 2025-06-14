import pygame

class Game:
    
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    STATIC_FPS = 60

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.update()

    def quit(self):
        self.running = False
        pygame.quit()

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
                return
        
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()))

        pygame.display.update()
        self.clock.tick(self.STATIC_FPS)