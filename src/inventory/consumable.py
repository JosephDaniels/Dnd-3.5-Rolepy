class Consumable:
    def __init__(self, name, description, restore_amount):
        self.name = name
        self.description = description
        self.restore_amount = restore_amount

    def apply(self, character):
        raise NotImplementedError("Consumable.apply must be implemented by subclasses")

class Food(Consumable):
    def apply(self, character):
        status = character.physical_status
        current = getattr(status, 'hunger', 0)
        max_val = getattr(status, 'max_hunger', 100)
        new_val = min(current + self.restore_amount, max_val)
        setattr(status, 'hunger', new_val)
        return f"{character.name} eats {self.name} and restores {self.restore_amount} hunger."

class Drink(Consumable):
    def apply(self, character):
        status = character.physical_status
        current = getattr(status, 'thirst', 0)
        max_val = getattr(status, 'max_thirst', 100)
        new_val = min(current + self.restore_amount, max_val)
        setattr(status, 'thirst', new_val)
        return f"{character.name} drinks {self.name} and restores {self.restore_amount} thirst."

# registry for all consumables
consumable_registry = {}

def register_consumable(item):
    consumable_registry[item.name.lower()] = item

def get_consumable(name):
    return consumable_registry.get(name.lower())

# example registrations
register_consumable(Food("Bread", "A simple loaf of bread.", 15))
register_consumable(Food("Apple", "A juicy red apple.", 10))
register_consumable(Drink("Water", "A bottle of clean water.", 20))
register_consumable(Drink("Ale", "A mug of frothy ale.", 15))
