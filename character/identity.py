# identity.py
# Core class referencing external data modules

from personality import Personality
from flaws import Flaws
from ideals import IDEALS
from bonds import BONDS
from backgrounds import BACKGROUNDS

class CharacterIdentity:
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
        for field in fields:
            default = [] if field == 'languages_spoken' else None
            setattr(self, field, kwargs.get(field, default))

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
