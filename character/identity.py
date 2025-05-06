
class CharacterIdentity:
    PERSONALITY_TRAITS = [
        "Brave", "Cautious", "Curious", "Impulsive", "Loyal",
        "Stoic", "Charming", "Blunt", "Optimistic", "Sarcastic",
        "Hot-headed", "Empathetic", "Pessimistic", "Ambitious"
    ]

    IDEALS = [
        "Justice", "Freedom", "Honor", "Power", "Knowledge",
        "Peace", "Revenge", "Redemption", "Faith", "Innovation",
        "Tradition", "Unity", "Chaos", "Balance"
    ]

    BONDS = [
        "Family", "Homeland", "Mentor", "Lover", "Oath",
        "Artifact", "Religion", "Guild", "Companion", "Debt"
    ]

    FLAWS = [
        "Greedy", "Vain", "Jealous", "Deceitful", "Arrogant",
        "Cowardly", "Wrathful", "Addicted", "Obsessive", "Naive"
    ]

    BACKGROUNDS = [
        "Acolyte", "Charlatan", "Criminal", "Entertainer", "Folk Hero",
        "Guild Artisan", "Hermit", "Noble", "Outlander", "Sage",
        "Sailor", "Soldier", "Urchin"
    ]
    def __init__(self, name="", race="", age=-1, gender="", alignment="", background="",
                 personality_traits="", ideals="", bonds="", flaws="", homeland="", faith="",
                 occupation="", languages_spoken=None, public_history="", private_history="",
                 eye_colour="", hair_colour="", skin_colour="", height="", weight="", build="",
                 notable_marks="", description=""):
        self.name = name
        self.race = race
        self.age = age
        self.gender = gender
        self.alignment = alignment
        self.background = background
        self.personality_traits = personality_traits
        self.ideals = ideals
        self.bonds = bonds
        self.flaws = flaws
        self.homeland = homeland
        self.faith = faith
        self.occupation = occupation
        self.languages_spoken = languages_spoken if languages_spoken is not None else []
        self.public_history = public_history
        self.private_history = private_history

        self.eye_colour = eye_colour
        self.hair_colour = hair_colour
        self.skin_colour = skin_colour
        self.height = height
        self.weight = weight
        self.build = build
        self.notable_marks = notable_marks
        self.description = description

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
