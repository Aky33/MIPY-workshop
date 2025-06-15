import pygame
import os

class AudioManager:
    def __init__(self, path):
        self.path = path
        self.playlist = self._load_playlist()
        self.current_track_index = 0
        self.volume_levels = [0.1, 0.04, 0]  # High, Low, Mute
        self.current_volume_index = 0  # Default to 10%
        
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_track_index])
            pygame.mixer.music.set_volume(self.volume_levels[self.current_volume_index])

    def _load_playlist(self):
        if not os.path.exists(self.path):
            print(f"Warning: Audio path not found at '{self.path}'")
            return []
        
        files = [os.path.join(self.path, f) for f in os.listdir(self.path) if f.endswith(('.mp3', '.wav', '.ogg'))]
        files.sort()
        return files

    def play(self):
        if self.playlist:
            pygame.mixer.music.play()

    def cycle_volume(self):
        """Přepne na další úroveň hlasitosti."""
        self.current_volume_index = (self.current_volume_index + 1) % len(self.volume_levels)
        pygame.mixer.music.set_volume(self.volume_levels[self.current_volume_index])

    def get_volume_state(self):
        """Vrátí aktuální stav hlasitosti pro výběr ikony."""
        if self.current_volume_index == 0:
            return "high"
        elif self.current_volume_index == 1:
            return "low"
        else:
            return "muted"

    def update(self):
        if not pygame.mixer.music.get_busy() and self.playlist:
            self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
            pygame.mixer.music.load(self.playlist[self.current_track_index])
            pygame.mixer.music.play()