async def do_additem(message, character):
    try:
        _, item = message.content.split(" ", 1)
    except ValueError:
        return "Usage: !additem <item>", message.channel
    character.inventory[item] = character.inventory.get(item, 0) + 1
    return f"Added 1x {item} to {character.name}'s inventory.", message.channel

async def do_removeitem(message, character):
    try:
        _, item = message.content.split(" ", 1)
    except ValueError:
        return "Usage: !removeitem <item>", message.channel
    if item not in character.inventory:
        return f"{item} not found in inventory.", message.channel
    del character.inventory[item]
    return f"Removed {item} from {character.name}'s inventory.", message.channel

async def do_equip(message, character):
    try:
        _, item = message.content.split(" ", 1)
    except ValueError:
        return "Usage: !equip <item>", message.channel
    if item not in character.inventory:
        return f"You don't have {item}.", message.channel
    character.equipment[item] = character.inventory.pop(item)
    return f"{character.name} equipped {item}.", message.channel

async def do_unequip(message, character):
    try:
        _, item = message.content.split(" ", 1)
    except ValueError:
        return "Usage: !unequip <item>", message.channel
    if item not in character.equipment:
        return f"{item} is not equipped.", message.channel
    character.inventory[item] = character.equipment.pop(item)
    return f"{character.name} unequipped {item}.", message.channel

async def do_inventory(message, character):
    inv_lines = [f"{k}: {v}" for k, v in character.inventory.items()]
    eq_lines = [f"{k}: {v}" for k, v in character.equipment.items()]
    lines = ["**Inventory**"] + inv_lines + ["**Equipment**"] + eq_lines
    return "\n".join(lines), message.channel
