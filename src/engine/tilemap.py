class Tilemap:
    def __init__(self, assets, tile_size = 32):
        self.assets = assets
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        # gets filled with grass
        for x in range(20):
            for y in range(20):
                self.tilemap[str(x) + ";" + str(y)] = {"type": "grass", "pos": (x, y)}

    def render(self, surf, offset=(0, 0)):

        for tile in self.offgrid_tiles:
            x = tile["pos"][0] - offset[0]
            y = tile["pos"][1] - offset[1]
            surf.blit(self.assets.tiles[tile["type"]], (x, y))
        
        beginX = offset[0] // self.tile_size
        endX = (offset[0] + surf.get_width()) // self.tile_size + 1
        beginY = offset[1] // self.tile_size
        endY = (offset[1] + surf.get_height()) // self.tile_size + 1
        for x in range(beginX, endX):
            for y in range(beginY, endY):
                loc =  f"{x};{y}"
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    xt = (tile["pos"][0] * self.tile_size) - offset[0]
                    yt = (tile["pos"][1] * self.tile_size) - offset[1]
                    surf.blit(self.assets.tiles[tile["type"]], (xt, yt))
        