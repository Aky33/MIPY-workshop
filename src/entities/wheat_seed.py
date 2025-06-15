from src.entities.seed import Seed
from src.entities.wheat import Wheat

class WheatSeed(Seed):
    def __init__(self, amount=1):
        super().__init__(amount)
        self.id = "wheatSeed"
        self.name = "Wheat Seeds"
        self.icon_asset = "wheatSeeds"
    
    def associated_plant():
        return Wheat((0, 0))