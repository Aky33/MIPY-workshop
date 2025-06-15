class Plant:
    # images represent growth stages of plant going from 0 (just planted) to 2 (fully grown)
    # growth time is in frames (assuming 60 FPS)
    def __init__(self, type, pos, images, growth_time = 600, growth_speed = 1):
        self.images = images
        self.growth_time = growth_time
        self.growth_speed = growth_speed
        self.progress = 0
        self.pos = pos
        self.harvested = False
        
    def update(self):
        self.progress += self.growth_speed
        
    def ready_to_harvest(self):
        return self.progress > self.growth_speed
    
    # To be implemented by child classes
    def get_item(self):
        return None

    def render(self, surf):
        if self.harvested: return
        stage = int((self.progress / self.growth_time) * len(self.images))
        stage = min(stage, len(self.images) - 1)
        surf.blit(self.images[stage], self.pos)