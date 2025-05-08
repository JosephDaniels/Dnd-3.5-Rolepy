class StatusEffect:
    def __init__(self, name, duration, on_apply=None, on_expire=None, on_turn=None):
        self.name = name
        self.duration = duration
        self.on_apply = on_apply
        self.on_expire = on_expire
        self.on_turn = on_turn

    def apply(self, target):
        if self.on_apply:
            self.on_apply(target)

    def expire(self, target):
        if self.on_expire:
            self.on_expire(target)

    def tick(self, target):
        if self.on_turn:
            self.on_turn(target)
        self.duration -= 1


class EffectManager:
    def __init__(self):
        self.status_effects = []

    def add_effect(self, effect, target):
        effect.apply(target)
        self.status_effects.append(effect)

    def update_effects(self, target):
        expired = []
        for effect in self.status_effects:
            effect.tick(target)
            if effect.duration <= 0:
                effect.expire(target)
                expired.append(effect)
        for effect in expired:
            self.status_effects.remove(effect)

    def has_effect(self, name):
        return any(effect.name == name for effect in self.status_effects)
