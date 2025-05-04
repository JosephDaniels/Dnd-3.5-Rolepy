from constitution import ConstitutionStatus
from mental import MentalStatus
from effects import EffectManager

class Entity:
    def __init__(self, name):
        self.name = name
        self.effects = EffectManager()
        self.constitution = ConstitutionStatus()
        self.mental = MentalStatus()

    def relieve(self):
        if self.constitution.bladder < 30:
            print(f"{self.name} doesn't need to go right now.")
        else:
            print(f"{self.name} relieves themselves. Sweet relief.")
            self.constitution.bladder = 0
            self.constitution.stamina = min(100, self.constitution.stamina + 5)
