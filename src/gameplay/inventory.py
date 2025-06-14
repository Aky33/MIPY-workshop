class Item:
    def __init__(self, id, name, icon_asset, amount=1):
        self.id = id
        self.name = name
        self.icon_asset = icon_asset
        self.amount = amount  # Fix: use the provided amount

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, amount={self.amount})"

class Inventory:
    def __init__(self):
        self.items = {}

    def addItem(self, item):
        if item.id in self.items:
            self.items[item.id].amount += item.amount  # Add the amount, not just 1
        else:
            self.items[item.id] = Item(item.id, item.name, item.icon_asset, item.amount)

    def removeItem(self, itemId, amount=1):
        if itemId in self.items:
            if self.items[itemId].amount > amount:
                self.items[itemId].amount -= amount
            elif self.items[itemId].amount == amount:
                del self.items[itemId]
            else:
                print(f"Not enough of item {itemId} to remove {amount}.")
        else:
            print(f"Item {itemId} isn't in the inventory")

    def getItem(self, item_id):
        return self.items.get(item_id, None)

    def listItems(self):
        return list(self.items.values())

