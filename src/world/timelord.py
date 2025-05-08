import datetime
import json
import random
from src.character.physical_status import PhysicalStatus
from src.character.mental_status import MentalStatus

class TimeLord:
    def __init__(self, world_state_file='world_state.json', debug=False):
        self.state_file = world_state_file
        self.debug = debug
        self._load_chronoscroll()
        self.physical_statuses = {"Rynn": PhysicalStatus()}
        self.mentals = {"Rynn": MentalStatus()}
        self.last_logged_hour = None
        self.internal_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

    def _load_chronoscroll(self):
        try:
            with open(self.state_file, 'r') as f:
                self.chronoscroll = json.load(f)
            if "journal" not in self.chronoscroll:
                self.chronoscroll["journal"] = {}
        except (FileNotFoundError, json.JSONDecodeError):
            self.chronoscroll = {
                "players": {},
                "journal": {}
            }

    def _save_chronoscroll(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.chronoscroll, f, indent=4)

    def mark_location(self, player_name, location):
        now = datetime.datetime.now().isoformat()
        self.chronoscroll["players"][player_name] = {
            "location": location,
            "last_seen": now
        }
        self._save_chronoscroll()

    def restore_passage(self, player_name):
        now = datetime.datetime.now()
        player = self.chronoscroll["players"].get(player_name)

        if not player:
            return f"⚠️ No timeline found for {player_name}."

        try:
            then = datetime.datetime.fromisoformat(player["last_seen"])
        except ValueError:
            return f"⚠️ Invalid timestamp for {player_name}."

        delta = now - then
        hours = int(delta.total_seconds() // 3600)

        prophecy = self._divine_changes(hours, player["location"])
        self.chronoscroll["players"][player_name]["last_seen"] = now.isoformat()
        self._save_chronoscroll()
        return prophecy

    def _divine_changes(self, hours, location):
        if hours < 1:
            return f"🕰️ Only moments passed in {location}. The veil remains undisturbed."
        elif hours < 6:
            return f"⏳ The shadows crept in {location}. The dust shifted. Whispers circled unseen corners."
        elif hours < 24:
            return f"🌒 In your absence, {location} breathed slowly. The night brought new sounds."
        else:
            return f"🌀 {hours} hours passed. In {location}, things changed. The world moved on without you."

    def journal_log_event(self, event_text, timestamp=None):
        if not timestamp:
            timestamp = self.internal_time.isoformat()
        self.chronoscroll["journal"][timestamp] = event_text
        self._save_chronoscroll()

    def simulate_hourly_tick(self):
        self.internal_time += datetime.timedelta(hours=1)
        iso_time = self.internal_time.isoformat()

        if iso_time == self.last_logged_hour:
            if self.debug:
                self.journal_log_event("(Skipped duplicate event log.)", timestamp=iso_time)
            return iso_time, "(Skipped duplicate event log.)"

        self.last_logged_hour = iso_time

        event = self._generate_random_event()
        self.journal_log_event(event, timestamp=iso_time)

        rynn_con = self.physical_statuses.get("Rynn")
        rynn_mental = self.mentals.get("Rynn")

        if rynn_con:
            for _ in range(10):
                rynn_con.update_per_round()

        if rynn_mental:
            for _ in range(10):
                rynn_mental.update_per_tick()

        assessment = self._hourly_assessment("Rynn", self.internal_time)
        return iso_time, assessment

    def simulate_round_tick(self):
        self.internal_time += datetime.timedelta(seconds=6)
        iso_time = self.internal_time.isoformat()
        event = self._generate_random_event()
        self.journal_log_event(event, timestamp=iso_time)

        rynn_con = self.physical_statuses.get("Rynn")
        rynn_mental = self.mentals.get("Rynn")

        if rynn_con:
            rynn_con.update_per_round()
        if rynn_mental:
            rynn_mental.update_per_tick()

        assessment = self._hourly_assessment("Rynn", self.internal_time)
        return iso_time, assessment

    def _hourly_assessment(self, name, in_game_time):
        real_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        mental = self.mentals.get(name)
        physical_status = self.physical_statuses.get(name)
        mood = mental.overall_mood() if mental else "Unknown"
        status = "Unknown"
        if physical_status:
            hunger = physical_status.hunger_state()
            thirst = physical_status.thirst_state()
            bladder = physical_status.bladder_state()
            stamina = f"{physical_status.stamina:.1f}"
            status = f"Hunger - {hunger}, Thirst - {thirst}, Bladder - {bladder}, Stamina - {stamina}"
        return f"[TimePulse] {real_time} | {in_game_time.isoformat()} | Mood: {mood} | {status}"

    def _generate_random_event(self):
        events = [
            "Minor tremor in the lower labs. Unclear cause.",
            "Bilgerat was seen entering the nursery chamber.",
            "A Dire Wolf howled in the west wing.",
            "The lights flickered for 3.2 seconds.",
            "Callista muttered something in an unknown tongue.",
            "A shadow moved independently of its caster.",
            "Someone whispered Rynn's name in the air duct."
        ]
        return random.choice(events)

if __name__ == '__main__':
    tl = TimeLord(debug=True)
    tl.mark_location("Rynn", "Cell 13: Blackwander - Pod Room")

    print("--- HOURLY TICK TEST ---")
    for i in range(3):
        timestamp, assessment = tl.simulate_hourly_tick()
        print(assessment)

    print("\n--- RAPID 6-SECOND TICK TEST ---")
    for i in range(10):
        timestamp, assessment = tl.simulate_round_tick()
        print(assessment)

    rynn_summary = tl.restore_passage("Rynn")
    print("\n--- TIME SKIP SUMMARY ---")
    print(rynn_summary)
