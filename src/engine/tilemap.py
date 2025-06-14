class Tilemap:
    def __init__(self, assets, tile_size = 32):
        self.assets = assets
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.farmland_count = 10
        self.farmlandX = 5
        self.farmlandY = 3
        self.max_col = 5
        self.farmland = {}

        self.generate_tilemap()
        
    def set_farmland_amt(self, amount):
        self.farmland_count = amount
        self.generate_tilemap()

    def add_plant(self, plant, pos):
        tileId = f"{pos[0]};{pos[1]}"
        if self.tilemap.get(tileId) == None:
            print("TileId not in tilemap", tileId)
            return False
        tile = self.tilemap[tileId]
        if tile["type"] != "farmland":
            print("TileId is not farmland")
            return False
        
        if tileId in self.farmland:
            print("TileId already has a plant")
            return False
        
        self.farmland[tileId] = plant
        real_pos = (pos[0] * self.tile_size, pos[1] * self.tile_size)
        plant.pos = real_pos
        return True
    
    def pixel_to_tile_pos(self, pos):
        return (pos[0] // self.tile_size, pos[1] // self.tile_size)

    def get_plant(self, pos):
        tileId = f"{pos[0]};{pos[1]}"
        tile = self.tilemap[tileId]
        if tile["type"] != "farmland":
            print("TileId is not farmland")
            return False
        
        if self.farmland.get(tileId) == None:
            return False
        
        return self.farmland[tileId]

    def harvest_plant(self, pos):
        tileId = f"{pos[0]};{pos[1]}"
        tile = self.tilemap[tileId]
        if tile["type"] != "farmland":
            print("TileId is not farmland")
            return False
        plant = self.farmland[tileId]
        plant.harvested = True
        self.remove_plant(pos)
        return plant

    def remove_plant(self, pos):
        tileId = f"{pos[0]};{pos[1]}"
        tile = self.tilemap[tileId]
        if tile["type"] != "farmland":
            print("TileId is not farmland")
            return False
        
        del self.farmland[tileId]

    def generate_tilemap(self):
        
        farmland_to_add = self.farmland_count
        for x in range(20):
            col = 0
            for y in range(20):
                can_place = farmland_to_add > 0 and col < self.max_col
                if self.farmlandX < x and self.farmlandY < y and can_place:
                    self.tilemap[str(x) + ";" + str(y)] = {"type": "farmland", "pos": (x, y)}
                    farmland_to_add -= 1
                    col += 1
                    continue
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
        