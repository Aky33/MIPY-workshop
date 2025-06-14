import pygame

BASE_IMG_PATH = "src/assets/"
TILE_SIZE = 32

class AssetManager:
    asset_path_list = {
        # use names of assets as keys and their paths as values
        # example: "grass": "tiles/grass.png"
    }

    asset_list = {

    }

    tileset_path = "tiles/ground_tiles.png"

    tiles = {

    }
        
    def __init__(self):
        for asset in self.asset_path_list:
            self.asset_list[asset] = self.load_image(self.asset_path_list[asset])
        self.prepare_tiles()

    def prepare_tiles(self):
        tileset = self.load_image(self.tileset_path)
        self.tiles["grass"] = tileset.subsurface(0, 0, TILE_SIZE, TILE_SIZE)

    def load_image(self, path):
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
        return img
