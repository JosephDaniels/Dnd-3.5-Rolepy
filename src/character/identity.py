# identity.py
# Core class referencing external data modules

from .personality import Personality
from .flaws import Flaws
from .ideals import IDEALS
from .bonds import BONDS
from .backgrounds import BACKGROUNDS


class CharacterIdentity:
    # Reference to all available traits, flaws, ideals, bonds, and backgrounds
    PERSONALITY_TRAITS = Personality.TRAITS
    FLAWS = Flaws.FLAWS
    IDEALS = IDEALS
    BONDS = BONDS
    BACKGROUNDS = BACKGROUNDS

    def __init__(self, **kwargs):
        fields = [
            'name', 'race', 'age', 'gender', 'alignment', 'background',
            'personality_traits', 'ideals', 'bonds', 'flaws', 'homeland', 'faith',
            'occupation', 'languages_spoken', 'public_history', 'private_history',
            'eye_colour', 'hair_colour', 'skin_colour', 'height', 'weight', 'build',
            'notable_marks', 'description'
        ]

        # Initialize fields, use provided kwargs or set default
        for field in fields:
            default = [] if field == 'languages_spoken' else None
            setattr(self, field, kwargs.get(field, default))

        # Initialize specific attributes for personality traits, flaws, ideals, and bonds
        self.personality_traits = kwargs.get('personality_traits', [])
        self.flaws = kwargs.get('flaws', [])
        self.ideals = kwargs.get('ideals', [])
        self.bonds = kwargs.get('bonds', [])
        self.background = kwargs.get('background', '')

    def to_dict(self):
        """Return the character's data as a dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data):
        """Create a CharacterIdentity instance from a dictionary."""
        return cls(**data)

    def __repr__(self):
        """String representation of the CharacterIdentity."""
        return f"CharacterIdentity(name={self.name}, personality_traits={self.personality_traits}, flaws={self.flaws}, ideals={self.ideals}, bonds={self.bonds}, background={self.background})"

    def get_personality(self):
        """Return the character's personality traits."""
        return [trait for trait in self.PERSONALITY_TRAITS if trait[0] in self.personality_traits]

    def get_flaws(self):
        """Return the character's flaws."""
        return [flaw for flaw in self.FLAWS if flaw[0] in self.flaws]

    def get_ideals(self):
        """Return the character's ideals."""
        return [ideal for ideal in self.IDEALS if ideal[0] in self.ideals]

    def get_bonds(self):
        """Return the character's bonds."""
        return [bond for bond in self.BONDS if bond[0] in self.bonds]

    def get_background(self):
        """Return the character's background."""
        return next((bg for bg in self.BACKGROUNDS if bg[0] == self.background), None)

