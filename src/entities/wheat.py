from src.entities.plant import Plant
from src.engine.asset_manager import AssetManager
from src.gameplay.inventory import Item

class Wheat(Plant):
    def __init__(self, pos, growth_time = 600, growth_speed = 1):
        super().__init__("wheat", pos, AssetManager().get_plant_images("wheat"), growth_time, growth_speed)

    def get_item():
        return Item("wheat", "Wheat", AssetManager().get_icon("wheat"))