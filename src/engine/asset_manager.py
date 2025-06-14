import pygame

BASE_IMG_PATH = "assets/"

class AssetManager:
    asset_path_list = {
        # use names of assets as keys and their paths as values
        # example: "grass": "tiles/grass.png"
    }

    asset_list = {

    }
        
    def __init__(self):
        for asset in self.asset_path_list:
            self.asset_list[asset] = self.load_image(self.asset_path_list[asset])

    def load_image(self, path):
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
        return img
