from src.entities.plant import Plant
from src.engine.asset_manager import AssetManager

class Carrot(Plant):
    def __init__(self, pos, growth_time = 600, growth_speed = 1):
        super().__init__("carrot", pos, AssetManager().get_plant_images("carrot"), growth_time, growth_speed)
