from src.entities.seed import Seed
from src.entities.wheat import Wheat
from src.engine.asset_manager import AssetManager

class WheatSeed(Seed):
    def __init__(self, amount=1):
        super().__init__(amount)
        self.id = "wheatSeed"
        self.name = "Wheat Seeds"
        self.icon_asset = AssetManager().get_seed_icon("wheatSeeds")
    
    def associated_plant():
        return Wheat((0, 0))