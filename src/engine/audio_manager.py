import pygame
import os

class AudioManager:
    def __init__(self, path):
        self.path = path
        self.playlist = self._load_playlist()
        self.current_track_index = 0
        
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_track_index])
            pygame.mixer.music.set_volume(0.05) # Nastavení výchozí hlasitosti na 5%

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

    def set_volume(self, volume):
        """Nastaví hlasitost hudby (0.0 až 1.0)"""
        if self.playlist:
            pygame.mixer.music.set_volume(volume)

    def update(self):
        if not pygame.mixer.music.get_busy() and self.playlist:
            self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
            pygame.mixer.music.load(self.playlist[self.current_track_index])
            pygame.mixer.music.play()