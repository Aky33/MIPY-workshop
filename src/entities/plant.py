class Plant:
    # images represent growth stages of plant going from 0 (just planted) to 2 (fully grown)
    # growth time is in frames (assuming 60 FPS)
    def __init__(self, pos, images, growth_time = 600, growth_speed = 1):
        self.images = images
        self.growth_time = growth_time
        self.growth_speed = growth_speed
        self.progress = 0
        self.pos = pos

    def update(self):
        self.progress += self.growth_speed
        
    def render(self, surf):
        stage = (round(self.progress // self.growth_time) * 3) - 1
        surf.blit(self.images[stage], self.pos)