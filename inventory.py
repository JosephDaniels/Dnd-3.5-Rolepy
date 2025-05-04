import json
from equipment import Item

class Inventory:
    def __init__(self):
        self.items = {}  # {item_name: [Item, quantity]}
        self.equipped = {}  # {slot: Item}
        self.capacity = 100.0  # Total weight capacity

    def add_item(self, item: Item, quantity=1):
        if item.name in self.items:
            self.items[item.name][1] += quantity
        else:
            self.items[item.name] = [item, quantity]

    def remove_item(self, item_name, quantity=1):
        if item_name in self.items:
            self.items[item_name][1] -= quantity
            if self.items[item_name][1] <= 0:
                del self.items[item_name]

    def equip_item(self, item_name, slot):
        if item_name not in self.items:
            return f"You don't have {item_name}."

        item, _ = self.items[item_name]
        if item.equip_slot != slot:
            return f"{item_name} cannot be equipped to {slot}."

        self.equipped[slot] = item
        self.remove_item(item_name)
        return f"Equipped {item_name} to {slot}."

    def unequip_item(self, slot):
        if slot not in self.equipped:
            return f"Nothing equipped in {slot}."

        item = self.equipped.pop(slot)
        self.add_item(item)
        return f"Unequipped {item.name} from {slot}."

    def total_weight(self):
        total = 0.0
        for item, qty in self.items.values():
            total += item.weight * qty
        return total

    def save(self, path):
        data = {
            "items": {name: [item.to_dict(), qty] for name, (item, qty) in self.items.items()},
            "equipped": {slot: item.to_dict() for slot, item in self.equipped.items()}
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.items = {name: [Item.from_dict(d), qty] for name, (d, qty) in data["items"].items()}
            self.equipped = {slot: Item.from_dict(d) for slot, d in data["equipped"].items()}

    def display(self):
        lines = ["Equipped:"]
        for slot, item in self.equipped.items():
            lines.append(f"  {slot.title()}: {item.name}")

        lines.append("\nInventory:")
        for name, (item, qty) in self.items.items():
            lines.append(f"  {name}: {qty} ({item.weight} lb each)")

        lines.append(f"\nTotal weight: {self.total_weight()} / {self.capacity} lb")
        return "\n".join(lines)
