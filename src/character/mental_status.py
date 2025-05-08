import random

THRESHOLD_LEVELS = [100, 85, 60, 40, 20, 0]

THRESHOLD_LABELS = {
    "focus": ["Hyperfocused", "Concentrated", "Engaged", "Distracted", "Scatterbrained", "Unfocused"],
    "hope": ["Radiant", "Hopeful", "Positive", "Stable", "Discouraged", "Hopeless"],
    "stress": ["Overwhelmed", "Panicked", "Worried", "Uneasy", "Tense", "Relaxed"],
    "happiness": ["Ecstatic", "Joyful", "Pleased", "Content", "Unhappy", "Miserable"],
    "sadness": ["Devastated", "Grieving", "Downcast", "Low", "Blue", "Untroubled"],
    "loneliness": ["Abandoned", "Yearning", "Alone", "Isolated", "Distant", "Connected"],
    "anger": ["Berserk", "Fuming", "Frustrated", "Irritated", "Annoyed", "Calm"],
    "shame": ["Crushed", "Humiliated", "Ashamed", "Embarrassed", "Self-aware", "Proud"],
    "fear": ["Terrified", "Panicked", "Scared", "Nervous", "Wary", "Fearless"],
    "boredom": ["Existential Crisis", "Listless", "Bored", "Restless", "Twitchy", "Engaged"],
    "relaxation": ["Blissed Out", "Tranquil", "Calm", "Tense", "Anxious", "Stressed"],
    "arousal": ["Climaxing", "Overstimulated", "Heated", "Aroused", "Aware", "Dormant"],
    "courage": ["Unshakable", "Bold", "Steady", "Wavering", "Doubtful", "Crushed"],
    "inspiration": ["Enlightened", "Motivated", "Sparked", "Flat", "Uninspired", "Burnt Out"],
    "curiosity": ["Obsessed", "Intrigued", "Interested", "Distracted", "Unfocused", "Disengaged"],
    "social": ["Overstimulated", "Fulfilled", "Connected", "Withdrawn", "Shy", "Isolated"],
    "disgust": ["Repulsed", "Grossed Out", "Offended", "Annoyed", "Irritated", "Unbothered"]
}

MOOD_EMOJIS = {
    "Happy": "😄", "Angry": "😡", "Bored": "😐", "Flirty": "😉", "Scared": "😱", "Sad": "😭",
    "Embarrassed": "😳", "Playful": "🎲", "Confident": "😎", "Uncomfortable": "😣",
    "Chillin'": "🧘", "Inspired": "💡", "Grateful": "🙏", "Loved": "❤️",
    "Paranoid": "🕵️", "Guilty": "😔", "Jealous": "😤", "Fine": "🙂"
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
    NEUTRAL_BARS = ["arousal"]
    POSITIVE_BARS = ["happiness", "relaxation", "courage", "inspiration", "curiosity", "social", "hope", "focus"]
    NEGATIVE_BARS = ["sadness", "loneliness", "anger", "shame", "fear", "boredom", "disgust", "stress"]

    def __init__(self):
        for attr in self.POSITIVE_BARS + self.NEGATIVE_BARS + self.NEUTRAL_BARS:
            setattr(self, attr, 50)

    def overall_mood(self):
        if self.happiness > 70 and self.anger < 10 and self.boredom < 20 and self.sadness < 20:
            return "Happy"
        elif self.anger > 60:
            return "Angry"
        elif self.boredom > 60:
            return "Bored"
        elif self.arousal > 50:
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
        elif self.hope > 70 and self.stress < 30 and self.relaxation > 60:
            return "Chillin'"
        elif self.hope > 70 and self.stress < 30:
            return "Inspired"
        elif self.relaxation > 70 and self.social > 50:
            return "Grateful"
        elif self.hope > 60 and self.social > 60 and self.happiness > 60:
            return "Loved"
        elif self.stress > 60 and self.fear > 40:
            return "Paranoid"
        elif self.fear > 30 and self.shame > 30:
            return "Guilty"
        elif self.social < 20 and self.loneliness > 50 and self.anger > 40:
            return "Jealous"
        else:
            return "Fine"

    def describe_state(self):
        mood = self.overall_mood()
        emoji = MOOD_EMOJIS.get(mood, "❓")
        commentary = {
            "Happy": "You feel like the world is on your side today.",
            "Angry": "Your blood is boiling, fists clenching without thinking.",
            "Bored": "You tap your fingers restlessly, begging for something new.",
            "Scared": "Your heart races—something doesn’t feel right.",
            "Sad": "A quiet heaviness lingers in your chest.",
            "Embarrassed": "You feel like everyone saw it—even if they didn’t.",
            "Chillin'": "The vibe is immaculate. Nothing can shake you."
        }.get(mood, "You feel... something.")
        return f"{emoji} Mood: {mood} — {commentary}"

    def update_per_tick(self):
        self.happiness = max(0, self.happiness - 0.033)
        self.sadness = min(100, self.sadness + 0.017)
        self.loneliness = min(100, self.loneliness + 0.033)
        self.anger = max(0, self.anger - 0.017)
        self.shame = max(0, self.shame - 0.017)
        self.fear = max(0, self.fear - 0.017)
        self.arousal = max(0, self.arousal - 0.017)
        self.boredom = min(100, self.boredom + 0.033)
        self.relaxation = max(0, min(100, self.relaxation - 0.017))
        self.courage = max(0, min(100, self.courage - 0.017))
        self.inspiration = max(0, min(100, self.inspiration - 0.017))
        self.curiosity = max(0, min(100, self.curiosity - 0.017))
        self.social = max(0, min(100, self.social - 0.017))
        self.disgust = max(0, min(100, self.disgust + 0.017))
        self.hope = max(0, min(100, self.hope - 0.017))
        self.focus = max(0, min(100, self.focus - 0.017))

        stress_change = 0.017
        if self.relaxation > 60:
            stress_change -= 0.017
        if self.happiness > 60:
            stress_change -= 0.017

        if self.fear > 50:
            self.stress = min(100, self.stress + 0.033)
            self.boredom = max(0, self.boredom - 0.017)
        if self.boredom > 60:
            self.stress = max(0, self.stress - 0.017)

        self.stress = min(100, max(0, self.stress + stress_change))

if __name__ == "__main__":
    mental = MentalStatus()

    for i in range(10):
        print(f"Tick {i+1}")
        mental.update_per_tick()
        print(mental.describe_state())
