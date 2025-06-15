from src.gameplay.inventory import Item
from src.entities.plant import Plant

class Seed(Item):

    def __init__(self, amount=1):
        super().__init__("defSeed", "default", "", amount)

    def associated_plant():
        return Plant("default", (0, 0), [])