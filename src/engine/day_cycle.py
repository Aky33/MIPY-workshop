import pygame

class DayCycle:
    def __init__(self, day_length_seconds=60):
        self.day_length = day_length_seconds  # celý den v sekundách
        self.time_elapsed = 0  # čas od začátku dne
        self.time_of_day = "morning"  # počáteční stav

    def update(self, dt):
        self.time_elapsed += dt
        cycle_progress = (self.time_elapsed % self.day_length) / self.day_length

        if cycle_progress < 0.25:
            self.time_of_day = "morning"
        elif cycle_progress < 0.5:
            self.time_of_day = "afternoon"
        elif cycle_progress < 0.75:
            self.time_of_day = "evening"
        else:
            self.time_of_day = "night"

    def get_overlay_color(self):
        """Vrací barvu pro světelný overlay podle denní doby."""
        overlays = {
            "morning": (255, 255, 255, 0),
            "afternoon": (255, 255, 224, 30),
            "evening": (255, 140, 0, 80),
            "night": (0, 0, 64, 120),
        }
        return overlays[self.time_of_day]
