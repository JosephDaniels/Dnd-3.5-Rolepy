import unittest
from unittest.mock import MagicMock, AsyncMock, patch
from src.dungeon_master.AIDM import AIDM

class DummyCtx:
    def __init__(self):
        self.guild = MagicMock()
        self.guild.id = 1234
        self.send = AsyncMock()

class DummyCharacter:
    def __init__(self, name, hp=10, ac=10):
        self.name = name
        self.current_health = hp
        self.armor_class = ac
        self.dying = False
        self.dead = False
        self.initiative = 0

    def get_initiative_bonus(self): return 2
    def get_melee_attack_bonus(self): return 3
    def get_ranged_attack_bonus(self): return 1

    def __lt__(self, other):
        return self.name < other.name

class TestAIDM(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.dungeon_master = AIDM(debug=False)
        self.hero = DummyCharacter("Hero", hp=20, ac=14)
        self.goblin = DummyCharacter("Goblin", hp=8, ac=12)

    def test_add_and_get_character(self):
        self.dungeon_master.add_character(self.hero)
        result = self.dungeon_master.get_character("Hero")
        self.assertEqual(result.name, "Hero")

    def test_combat_round_order(self):
        self.dungeon_master.roll_initiative = MagicMock(return_value=15)
        self.dungeon_master.start_combat([self.hero, self.goblin])
        self.assertEqual(len(self.dungeon_master.battle_order), 2)
        self.assertTrue(self.dungeon_master.in_combat)

    def test_turn_rotation(self):
        self.dungeon_master.battle_order = [(15, self.hero), (12, self.goblin)]
        self.dungeon_master.current_combatant = 0
        self.dungeon_master.current_round = 1
        self.dungeon_master.do_next_turn()
        self.assertEqual(self.dungeon_master.current_combatant, 1)
        self.dungeon_master.do_next_turn()
        self.assertEqual(self.dungeon_master.current_combatant, 0)
        self.assertEqual(self.dungeon_master.current_round, 2)

    def test_attack_logic(self):
        hit = self.dungeon_master.do_attack(self.hero, self.goblin)
        self.assertIsInstance(hit, bool)

    def test_deal_damage_logic(self):
        self.dungeon_master.deal_damage(self.hero, self.goblin, 5)
        self.assertEqual(self.goblin.current_health, 3)
        self.dungeon_master.deal_damage(self.hero, self.goblin, 5)
        self.assertTrue(self.goblin.dying)

    @patch("openai.AsyncOpenAI")
    async def test_ask_response(self, mock_openai):
        dummy_response = AsyncMock()
        dummy_response.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="Test DM reply"))
        ]
        mock_openai.return_value = dummy_response

        ctx = DummyCtx()
        reply = await self.dungeon_master.ask("What do I see?", ctx)
        self.assertEqual(reply, "Test DM reply")
        ctx.send.assert_called_once_with("\U0001f9e0 AIDM is thinking...")

if __name__ == '__main__':
    unittest.main()
