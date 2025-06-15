from src.entities.plant import Plant
from src.engine.asset_manager import AssetManager
from src.engine.inventory import Item

class Carrot(Plant):
    def __init__(self, pos, growth_time = 600, growth_speed = 1):
        super().__init__("carrot", pos, AssetManager().get_plant_images("carrot"), growth_time, growth_speed)

    def get_item(self):
        return Item("carrot", "Carrot", AssetManager().get_icon("carrot"), price=30)
    
    def associated_seed(self):
        from src.entities.carrot_seed import CarrotSeed
        return CarrotSeed()
