from src.entities.seed import Seed
from src.entities.carrot import Carrot
from src.engine.asset_manager import AssetManager

class CarrotSeed(Seed):
    def __init__(self, amount=1):
        super().__init__(amount)
        self.id = "carrotSeed"
        self.name = "Carrot Seeds"
        self.icon_asset = AssetManager().get_seed_icon("carrotSeeds")
    
    def associated_plant():
        return Carrot((0, 0))