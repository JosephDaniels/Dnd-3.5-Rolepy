# inventory_commands.py

async def do_additem(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        return "You're not logged in!", message.channel

    try:
        _, item, qty = message.content.split(" ", 2)
        qty = int(qty)
    except ValueError:
        return "Usage: !additem <item> <quantity>", message.channel

    character = dm.logged_in_as[username]
    key = item.lower()

    if not hasattr(character, "inventory"):
        character.inventory = {}

    if key in character.inventory:
        original, count = character.inventory[key]
        character.inventory[key] = (original, count + qty)
    else:
        character.inventory[key] = (item, qty)

    return f"Added {qty}x {item} to {character.username}'s inventory.", message.channel


async def do_removeitem(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        return "You're not logged in!", message.channel

    try:
        _, item, qty = message.content.split(" ", 2)
        qty = int(qty)
    except ValueError:
        return "Usage: !removeitem <item> <quantity>", message.channel

    character = dm.logged_in_as[username]
    key = item.lower()

    if not hasattr(character, "inventory") or key not in character.inventory:
        return f"{character.username} doesn't have any {item}.", message.channel

    original, count = character.inventory[key]
    if qty >= count:
        del character.inventory[key]
        return f"Removed all of {original} from {character.username}'s inventory.", message.channel
    else:
        character.inventory[key] = (original, count - qty)
        return f"Removed {qty}x {original} from {character.username}'s inventory.", message.channel


async def do_equip(message, dm):
    character = dm.logged_in_as[f"{message.author.name}#{message.author.discriminator}"]
    _, item, slot = message.content.split(" ", 2)

    # Just throw the item into the designated slot
    character.body_slots[slot.lower()].append({
        "item": item,
        "description": "No description yet."
    })

    character.save_to_json()
    return f"{character.name} equips {item} to {slot}.", message.channel

async def do_unequip(message, dm):
    args = message.content.split()
    if len(args) < 2:
        return "Please specify the slot to unequip. Example: `!unequip right_hand`"

    slot = args[1].lower()

    char = dm.get(message.author.id)  # or dm_helper.lookup(message.author.id), whatever your helper uses
    # char = get_character_by_user(message.author.id)  # However you're fetching the character
    if slot not in char.body_slots:
        return f"'{slot}' is not a valid equipment slot."

    if not char.body_slots[slot]:
        return f"Nothing is equipped in the {slot.replace('_', ' ')} slot."

    char.unequip_item(slot)
    char.save_to_json()
    return f"{char.name} has unequipped their gear from the {slot.replace('_', ' ')} slot."
async def do_inventory(message, dm):
    character = dm.logged_in_as[f"{message.author.name}#{message.author.discriminator}"]
    lines = []

    # Show equipped items from body_slots
    lines.append(f"**{character.name}'s Equipped Gear:**")
    for slot, items in character.body_slots.items():
        if items:
            for i, item in enumerate(items):
                item_name = item.get("item", "Unknown")
                lines.append(f"- {slot.title()} slot with {item_name} equipped.")

    # Show inventory
    lines.append(f"\n**Inventory:**")
    if hasattr(character, "inventory") and character.inventory:
        for key, value in character.inventory.items():
            if isinstance(value, tuple):
                name, qty = value
            else:
                name = key
                qty = value
            lines.append(f"- {name}: {qty}")
    else:
        lines.append("Inventory is empty.")

    return "\n".join(lines), message.channel
