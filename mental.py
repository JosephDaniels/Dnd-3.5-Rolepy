# mental.py

THRESHOLD_LEVELS = [100, 85, 60, 40, 20, 0]

THRESHOLD_LABELS = {
    "happiness":     ["Ecstatic", "Joyful", "Pleased", "Content", "Unhappy", "Miserable"],
    "sadness":       ["Devastated", "Grieving", "Downcast", "Low", "Blue", "Untroubled"],
    "loneliness":    ["Abandoned", "Yearning", "Alone", "Isolated", "Distant", "Connected"],
    "anger":         ["Berserk", "Fuming", "Frustrated", "Irritated", "Annoyed", "Calm"],
    "shame":         ["Crushed", "Humiliated", "Ashamed", "Embarrassed", "Self-aware", "Proud"],
    "fear":          ["Terrified", "Panicked", "Scared", "Nervous", "Wary", "Fearless"],
    "boredom":       ["Existential Crisis", "Listless", "Bored", "Restless", "Twitchy", "Engaged"],
    "relaxation":    ["Blissed Out", "Tranquil", "Calm", "Tense", "Anxious", "Stressed"],
    "arousal":       ["Climaxing", "Overstimulated", "Heated", "Aroused", "Aware", "Dormant"],
    "confidence":    ["Unshakable", "Bold", "Steady", "Wavering", "Doubtful", "Crushed"],
    "inspiration":   ["Enlightened", "Motivated", "Sparked", "Flat", "Uninspired", "Burnt Out"],
    "curiosity":     ["Obsessed", "Intrigued", "Interested", "Distracted", "Unfocused", "Disengaged"],
    "social":        ["Overstimulated", "Fulfilled", "Connected", "Withdrawn", "Shy", "Isolated"],
    "disgust":       ["Repulsed", "Grossed Out", "Offended", "Annoyed", "Irritated", "Unbothered"]
}

def evaluate_state(value, labels=None):
    if isinstance(labels, str):
        labels = THRESHOLD_LABELS.get(labels, ["Max", "High", "Mid", "Low", "Very Low", "Empty"])
    thresholds = [(t, l) for t, l in zip(THRESHOLD_LEVELS, labels)]
    for threshold, label in thresholds:
        if value >= threshold:
            return label
    return thresholds[-1][1]

class MentalStatus:
    POSITIVE_BARS = ["happiness", "relaxation", "arousal", "confidence", "inspiration", "curiosity", "social"]
    NEGATIVE_BARS = ["sadness", "loneliness", "anger", "shame", "fear", "boredom", "disgust"]

    def __init__(self):
        self.happiness = 50
        self.sadness = 0
        self.loneliness = 0
        self.anger = 0
        self.shame = 0
        self.fear = 0
        self.boredom = 0
        self.relaxation = 50
        self.arousal = 0
        self.confidence = 50
        self.inspiration = 50
        self.curiosity = 50
        self.social = 50
        self.disgust = 0

    def update_per_round(self):
        self.happiness = max(0, self.happiness - 0.2)
        self.sadness = min(100, self.sadness + 0.1)
        self.loneliness = min(100, self.loneliness + 0.2)
        self.anger = max(0, self.anger - 0.1)
        self.shame = max(0, self.shame - 0.1)
        self.fear = max(0, self.fear - 0.1)
        self.arousal = max(0, self.arousal - 0.1)
        self.boredom = min(100, self.boredom + 0.2)
        self.relaxation = max(0, min(100, self.relaxation - 0.1))
        self.confidence = max(0, min(100, self.confidence - 0.1))
        self.inspiration = max(0, min(100, self.inspiration - 0.1))
        self.curiosity = max(0, min(100, self.curiosity - 0.1))
        self.social = max(0, min(100, self.social - 0.1))
        self.disgust = max(0, min(100, self.disgust + 0.1))

    def overall_mood(self):
        if self.happiness > 70 and self.anger < 10 and self.boredom < 20 and self.sadness < 20:
            return "Happy"
        elif self.anger > 60:
            return "Angry"
        elif self.boredom > 60:
            return "Bored"
        elif self.arousal > 50 and self.loneliness < 40:
            return "Flirty"
        elif self.fear > 60:
            return "Scared"
        elif self.sadness > 60:
            return "Sad"
        elif self.fear > 40 and self.shame > 40:
            return "Embarrassed"
        elif self.boredom < 20 and self.arousal < 30 and self.happiness > 60:
            return "Playful"
        elif self.happiness > 60 and self.fear < 20 and self.sadness < 20:
            return "Confident"
        elif self.happiness < 30 and self.fear > 30 and self.sadness > 40:
            return "Uncomfortable"
        else:
            return "Fine"

if __name__ == "__main__":
    mental = MentalStatus()
    for attr in MentalStatus.POSITIVE_BARS + MentalStatus.NEGATIVE_BARS:
        value = getattr(mental, attr)
        label = evaluate_state(value, attr)
        print(f"{attr.capitalize()}: {value} -> {label}")

    print("\nOverall Mood:", mental.overall_mood())
