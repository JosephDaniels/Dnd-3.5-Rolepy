import asyncio

from DM_helper import DM_helper, Character
from src.commands.user_commands import do_login, do_logout, do_status, do_whoami, do_profile
from src.commands.inventory_commands import do_additem, do_removeitem, do_equip, do_unequip, do_inventory
from src.commands.dice_commands import do_roll, do_coinflip
from src.commands.npc_commands import NPCCommands
from src.commands.combat_commands import CombatCommands
from src.commands.scene_commands import SceneCommands

# Dummy context and message classes for testing
class DummyChannel:
    def __init__(self):
        self.messages = []
    async def send(self, content=None, **kwargs):
        self.messages.append(content)

class DummyAuthor:
    def __init__(self, name, discriminator):
        self.name = name
        self.discriminator = discriminator

class DummyMessage:
    def __init__(self, content, author, channel):
        self.content = content
        self.author = author
        self.channel = channel

async def test_user_commands(dm):
    print("Testing User Commands")
    chan = DummyChannel()
    author = DummyAuthor('TestUser', '0001')

    # Login
    msg = DummyMessage('!login rynn_dragonwhisper', author, chan)
    res = await do_login(msg, dm)
    print(res)

    # Status
    msg.content = '!status'
    res = await do_status(msg, dm)
    print(res[0])

    # Whoami
    msg.content = '!whoami'
    res = await do_whoami(msg, dm)
    print(res[0])

    # Profile (will send to channel)
    msg.content = '!profile'
    await do_profile(msg, dm)
    print(chan.messages[-1] if chan.messages else 'No profile text')

    # Logout
    msg.content = '!logout'
    res = await do_logout(msg, dm)
    print(res)

async def test_inventory_commands(dm):
    print("\nTesting Inventory Commands")
    chan = DummyChannel()
    author = DummyAuthor('TestUser', '0001')
    character = Character.from_json('character_sheets/rynn_delon_dragonwhisper.json')

    # Add item
    msg = DummyMessage('!additem sword', author, chan)
    res = await do_additem(msg, character)
    print(res)

    # Inventory list
    msg.content = '!inventory'
    res = await do_inventory(msg, character)
    print(res[0])

    # Equip
    msg.content = '!equip sword'
    res = await do_equip(msg, character)
    print(res)

    # Unequip
    msg.content = '!unequip sword'
    res = await do_unequip(msg, character)
    print(res)

    # Remove item
    msg.content = '!removeitem sword'
    res = await do_removeitem(msg, character)
    print(res)

async def test_dice_commands():
    print("\nTesting Dice Commands")
    chan = DummyChannel()
    author = DummyAuthor('TestUser', '0001')
    msg = DummyMessage('!roll 2d6+1', author, chan)
    res = await do_roll(msg)
    print(res)

    msg.content = '!coinflip'
    res = await do_coinflip(msg)
    print(res)

async def test_npc_commands(bot):
    print("\nTesting NPC Commands")
    chan = DummyChannel()
    author = DummyAuthor('TestUser', '0001')
    ctx = type('ctx', (), {'send': chan.send, 'guild': type('g', (), {'id': 1}), 'author': author})
    cmds = NPCCommands(bot)

    await cmds.create_npc(ctx, npc_text="Goblin Merchant")
    await cmds.list_npcs(ctx)
    await cmds.npc_detail(ctx, index=1)
    print(chan.messages)

async def test_combat_commands(bot):
    print("\nTesting Combat Commands")
    chan = DummyChannel()
    author = DummyAuthor('TestUser', '0001')
    ctx = type('ctx', (), {'send': chan.send, 'author': author})
    cmds = CombatCommands(bot)

    await cmds.attack(ctx, target="goblin")
    await cmds.defend(ctx)
    await cmds.hide(ctx)
    print(chan.messages)

async def test_scene_commands(bot):
    print("\nTesting Scene Commands")
    chan = DummyChannel()
    author = DummyAuthor('TestUser', '0001')
    ctx = type('ctx', (), {'send': chan.send, 'guild': type('g', (), {'id': 1}), 'author': author})
    cmds = SceneCommands(bot)

    await cmds.set_scene(ctx, scene_name="Forest")
    await cmds.describe_scene(ctx, description="Tall trees everywhere.")
    await cmds.show_scene(ctx)
    await cmds.set_background(ctx, url="http://bg.url")
    await cmds.show_background(ctx)
    await cmds.set_map(ctx, map_url="http://map.url")
    await cmds.show_map(ctx)
    await cmds.reset_scene(ctx)
    print(chan.messages)

async def main():
    dm = DM_helper()
    bot = type('b', (), {})()

    await test_user_commands(dm)
    await test_inventory_commands(dm)
    await test_dice_commands()
    await test_npc_commands(bot)
    await test_combat_commands(bot)
    await test_scene_commands(bot)

if __name__ == '__main__':
    asyncio.run(main())
