class MentalStatus:
    def __init__(self):
        self.happiness = 50
        self.sadness = 0
        self.loneliness = 0
        self.anger = 0
        self.shame = 0
        self.fear = 0
        self.arousal = 0
        self.boredom = 0

    def arousal_state(self):
        a = self.arousal
        if a <= 5:
            return "Dormant"
        elif a <= 20:
            return "Aware"
        elif a <= 50:
            return "Aroused"
        elif a <= 80:
            return "Heated"
        elif a < 100:
            return "Overstimulated"
        else:
            return "Climaxing"

    def boredom_state(self):
        b = self.boredom
        if b <= 10:
            return "Engaged"
        elif b <= 30:
            return "Restless"
        elif b <= 60:
            return "Bored"
        elif b <= 85:
            return "Listless"
        elif b < 100:
            return "Numb"
        else:
            return "Existential Crisis"

    def happiness_state(self):
        h = self.happiness
        if h <= 10:
            return "Miserable"
        elif h <= 30:
            return "Unhappy"
        elif h <= 60:
            return "Content"
        elif h <= 85:
            return "Pleased"
        elif h < 100:
            return "Joyful"
        else:
            return "Ecstatic"

    def sadness_state(self):
        s = self.sadness
        if s <= 10:
            return "Untroubled"
        elif s <= 30:
            return "Low"
        elif s <= 60:
            return "Downcast"
        elif s <= 85:
            return "Grieving"
        elif s < 100:
            return "Depressed"
        else:
            return "Devastated"

    def loneliness_state(self):
        l = self.loneliness
        if l <= 10:
            return "Connected"
        elif l <= 30:
            return "Distant"
        elif l <= 60:
            return "Isolated"
        elif l <= 85:
            return "Alone"
        elif l < 100:
            return "Yearning"
        else:
            return "Abandoned"

    def anger_state(self):
        a = self.anger
        if a <= 10:
            return "Calm"
        elif a <= 30:
            return "Annoyed"
        elif a <= 60:
            return "Irritated"
        elif a <= 85:
            return "Fuming"
        elif a < 100:
            return "Enraged"
        else:
            return "Berserk"

    def shame_state(self):
        s = self.shame
        if s <= 10:
            return "Proud"
        elif s <= 30:
            return "Self-aware"
        elif s <= 60:
            return "Embarrassed"
        elif s <= 85:
            return "Ashamed"
        elif s < 100:
            return "Humiliated"
        else:
            return "Crushed"

    def fear_state(self):
        f = self.fear
        if f <= 10:
            return "Fearless"
        elif f <= 30:
            return "Wary"
        elif f <= 60:
            return "Nervous"
        elif f <= 85:
            return "Scared"
        elif f < 100:
            return "Panicked"
        else:
            return "Terrified"
