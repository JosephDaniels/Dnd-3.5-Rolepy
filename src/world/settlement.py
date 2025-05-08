class Settlement:
    def __init__(self, name, settlement_type, population=0, biome=None, features=None, notes=""):
        self.name = name
        self.settlement_type = settlement_type
        self.population = population
        self.biome = biome
        self.features = features or []
        self.notes = notes

    def add_feature(self, feature):
        self.features.append(feature)

    def describe(self):
        return {
            "name": self.name,
            "type": self.settlement_type,
            "population": self.population,
            "biome": self.biome,
            "features": self.features,
            "notes": self.notes
        }