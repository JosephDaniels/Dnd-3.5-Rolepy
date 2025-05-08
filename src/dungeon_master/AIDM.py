from src.games.rolepy_dice import *
import openai
import os
from src.commands.scene_commands import scene_registry, scene_descriptions

class AIDM(object):
    def __init__(self, debug=True):
        self.debug = debug
        self.characters = {}
        self.logged_in = set()
        self.active_sessions = {}
        self.logged_in_as = {}

        self.in_combat = False
        self.battle_order = []
        self.current_round = 0
        self.current_combatant = 0

        openai.api_key = os.getenv("OPENAI_API_KEY")

    def save_logins(self):
        with open("../../data/logged_in.txt", mode='w+', encoding="utf-8") as f:
            for key in self.logged_in_as.keys():
                f.write(f"{key} = {self.logged_in_as[key].name}\n")

    def add_character(self, character_sheet):
        self.characters[character_sheet.name] = character_sheet

    def get_character(self, character_name=""):
        return self.characters.get(character_name)

    def start_combat(self, combatants):
        self.in_combat = True
        self.current_round = 1
        self.current_combatant = 0
        temp_battle_order = []
        for combatant in combatants:
            initiative_result = self.roll_initiative(combatant)
            temp_battle_order.append((initiative_result, combatant))
        self.battle_order = sorted(temp_battle_order, reverse=True)

    def roll_initiative(self, initiator):
        bonus = initiator.get_initiative_bonus()
        roll = rolld(20)
        result = roll + bonus
        if self.debug:
            print(f"{initiator.name} rolled initiative: {roll} + {bonus} = {result}")
        return result

    def whose_turn_isit(self):
        return self.battle_order[self.current_combatant][1].name

    def do_next_turn(self):
        self.current_combatant += 1
        if self.current_combatant >= len(self.battle_order):
            self.current_combatant = 0
            self.current_round += 1

    def do_attack(self, attacker, target, attack_type="melee"):
        roll = rolld(20)
        if attack_type == "melee":
            bonus = attacker.get_melee_attack_bonus()
        elif attack_type == "ranged":
            bonus = attacker.get_ranged_attack_bonus()
        else:
            raise ValueError("Unknown attack type")

        total = roll + bonus
        if self.debug:
            print(f"{attacker.name} attacks {target.name}: {roll} + {bonus} = {total} vs AC {target.armor_class}")

        return total > target.armor_class

    def deal_damage(self, attacker, victim, damage):
        victim.current_health -= damage
        if self.debug:
            print(f"{attacker.name} deals {damage} to {victim.name} (HP left: {victim.current_health})")
        if victim.current_health <= 0:
            victim.dying = True
            if victim.current_health <= -10:
                victim.dead = True
                victim.dying = False
            if self.debug:
                status = "dead" if victim.dead else "dying"
                print(f"{victim.name} is now {status}.")

    async def ask(self, prompt, ctx=None):
        if ctx:
            await ctx.send("🧠 AIDM is thinking...")

        scene_context = ""
        if ctx and ctx.guild:
            scene_name = scene_registry.get(ctx.guild.id)
            scene_desc = scene_descriptions.get(ctx.guild.id)
            if scene_name:
                scene_context = f"You are currently in the scene called '{scene_name}'."
                if scene_desc:
                    scene_context += f"\nScene Description: {scene_desc}"

        from openai import AsyncOpenAI
        client = AsyncOpenAI()

        try:
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a dungeon_master for a gritty dark fantasy D&D 3.5e game. Respond vividly and concisely."},
                    {"role": "user", "content": scene_context + "\n" + prompt if scene_context else prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error generating DM response: {e}]"

    def get_status_summary(self, character):
        mood = character.mental_status.overall_mood() if isinstance(character.mental_status, MentalStatus) else "Unknown"
        if isinstance(character.physical_status, PhysicalStatus):
            hunger = character.physical_status.hunger_state()
            thirst = character.physical_status.thirst_state()
            bladder = character.physical_status.bladder_state()
            stamina = f"{character.physical_status.stamina:.1f}"
            return f"Mood: {mood} | Hunger - {hunger}, Thirst - {thirst}, Bladder - {bladder}, Stamina - {stamina}"
        return f"Mood: {mood} | Hunger: Unknown | Thirst: Unknown | Bladder: Unknown | Stamina: Unknown"
