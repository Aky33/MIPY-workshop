import pygame
import os
import numpy as np

class Player:
    def __init__(self, position_x, position_y, width, height, speed, screen_width, screen_height):
        self.image = pygame.image.load(
            os.path.join("src", "assets", "sprites", "player", "farmer_idle.png")
        ).convert_alpha()

        self.rect = pygame.Rect(position_x, position_y, width, height)
        self.speed = speed
        self.exp = 0
        self.fitness = 1
        self.energy = 100

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.interacting = False

        self.food = 3
        self.idle_ticks = 0

        self.anim_index = 0
        self.anim_timer = 0
        self.anim_delay = 10
        self.last_dir = "down"

        self.animations = {
            "down": [
                pygame.image.load(os.path.join("src", "assets", "sprites", "player", "walk_down_1.png")).convert_alpha(),
                pygame.image.load(os.path.join("src", "assets", "sprites", "player", "walk_down_2.png")).convert_alpha()
            ],
            "up": [
                pygame.image.load(os.path.join("src", "assets", "sprites", "player", "walk_up_1.png")).convert_alpha(),
                pygame.image.load(os.path.join("src", "assets", "sprites", "player", "walk_up_2.png")).convert_alpha()
            ],
            "left": [
                pygame.image.load(os.path.join("src", "assets", "sprites", "player", "walk_left.png")).convert_alpha(),
                pygame.image.load(os.path.join("src", "assets", "sprites", "player", "walk_left_down.png")).convert_alpha()
            ],
            "right": [
                pygame.image.load(os.path.join("src", "assets", "sprites", "player", "walk_right.png")).convert_alpha(),
                pygame.image.load(os.path.join("src", "assets", "sprites", "player", "walk_right_down.png")).convert_alpha()
            ],
            "idle": {
                "down": pygame.image.load(os.path.join("src", "assets", "sprites", "player", "farmer_idle.png")).convert_alpha(),
                "up": pygame.image.load(os.path.join("src", "assets", "sprites", "player", "farmer_idle_up.png")).convert_alpha(),
                "left": pygame.image.load(os.path.join("src", "assets", "sprites", "player", "farmer_idle_left.png")).convert_alpha(),
                "right": pygame.image.load(os.path.join("src", "assets", "sprites", "player", "farmer_idle_right.png")).convert_alpha()
            },
            
        }
        self.is_moving = False

    def handle_input(self, keys):
        self.interacting = keys[pygame.K_SPACE]
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        vec = np.array([dx, dy])
        if vec.any():
            vec = vec / np.linalg.norm(vec)

            # Zistenie smeru
            if abs(dx) > abs(dy):
                self.last_dir = "right" if dx > 0 else "left"
            else:
                self.last_dir = "down" if dy > 0 else "up"

        return vec[0] * self.speed, vec[1] * self.speed

    def move(self, dx, dy, obstacles):
        self.is_moving = False
        if dx == 0 and dy == 0 or self.energy <= 0:
            self.idle_ticks += 1
            if self.idle_ticks > 180:
                self.energy = min(100, self.energy + 0.001 * self.fitness)
            return False
        else:
            self.idle_ticks = 0

        next_position = self.rect.move(dx, dy)

        if (next_position.left < 0 or
            next_position.right > self.screen_width or
            next_position.top < 0 or
            next_position.bottom > self.screen_height):
            return False

        for obstacle in obstacles:
            if next_position.colliderect(obstacle):
                return False

        self.rect = next_position
        self.is_moving = True
        self.exp += 1
        self.energy = max(0, self.energy - 0.2)

        if self.exp >= 100:
            self.exp = 0
            self.fitness += 1
            self.energy = min(100, self.energy + 10)

        return True

    def harvest(self):
        """Volá se při sklizni rostliny"""
        # Sklizeň je náročná činnost
        base_cost = 10.0  # základní náklady na energii
        fitness_modifier = 0.25  # každý bod fitness snižuje náklady
        min_cost = 4.0

        energy_cost = max(min_cost, base_cost - self.fitness * fitness_modifier)

        if self.energy < energy_cost:
            print(f"Nemáš dost energie na sklizeň! Potřebuješ alespoň {energy_cost:.1f}, máš {self.energy:.1f}.")
            return

        # EXP a fitness zisk závisí na aktuální únavě
        exp_gain = int(8 + (100 - self.energy) / 8)
        fitness_gain = 1 if self.energy < 20 else 0

        self.energy -= energy_cost
        self.exp += exp_gain

        if self.exp >= 100:
            self.exp = 0
            self.fitness += 1
            print(f"Level UP! Nová úroveň fitness: {self.fitness}")
        elif fitness_gain:
            self.fitness += 1
            print("Získal jsi fitness bod za sklizeň s nízkou energií.")

        print(f"Sklizeno! -{energy_cost:.1f} energie, +{exp_gain} EXP")

    def get_required_energy_for_harvest(self):
        """Vrací aktuální náklady energie na sklizeň."""
        base_cost = 10.0
        fitness_modifier = 0.25
        min_cost = 4.0
        return max(min_cost, base_cost - self.fitness * fitness_modifier)

    def eat(self, amount=50):
        if self.food > 0:
            self.food -= 1
            self.energy = min(100, self.energy + amount)
            print(f"Jídlo snědeno. Energie: {self.energy}, Zbývá jídlo: {self.food}")
        else:
            print("Nemáš žádné jídlo!")

    def sleep(self):
        if self.energy < 100:
            self.energy = min(100, self.energy + 30)
            print(f"Spánek doplnil energii: {self.energy}")
        else:
            print("Energie už je plná, spánek není potřeba.")

    def render(self, surface, debug=False):
        offset_x = -10
        offset_y = -12

        moving = self.is_moving  # detekcia pohybu

        if moving:
            frames = self.animations.get(self.last_dir, [])
            if len(frames) > 1:
                self.anim_timer += 1
                if self.anim_timer >= self.anim_delay:
                    self.anim_index = (self.anim_index + 1) % len(frames)
                    self.anim_timer = 0
                self.image = frames[self.anim_index]
            elif len(frames) == 1:
                self.image = frames[0]
        else:
            if self.last_dir in self.animations["idle"]:
                self.image = self.animations["idle"][self.last_dir]
            else:
                base_dir = self.last_dir.split("_")[0]
                self.image = self.animations["idle"].get(base_dir, self.image)


        surface.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        if debug:
            pygame.draw.rect(surface, (255, 255, 0, 150), self.rect)
