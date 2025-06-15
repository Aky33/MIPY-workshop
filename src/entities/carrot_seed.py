from src.entities.seed import Seed
from src.entities.carrot import Carrot

class CarrotSeed(Seed):
    def __init__(self, amount=1):
        super().__init__(amount)
        self.id = "carrotSeed"
        self.name = "Carrot Seeds"
        self.icon_asset = "carrotSeeds"
    
    def associated_plant():
        return Carrot((0, 0))