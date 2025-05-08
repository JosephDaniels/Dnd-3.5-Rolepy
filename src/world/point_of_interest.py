class PointOfInterest:
    def __init__(self, name, poi_type, region=None, biome=None, danger_level=0, description=""):
        self.name = name
        self.poi_type = poi_type
        self.region = region
        self.biome = biome
        self.danger_level = danger_level
        self.description = description

    def describe(self):
        return {
            "name": self.name,
            "type": self.poi_type,
            "region": self.region,
            "biome": self.biome,
            "danger_level": self.danger_level,
            "description": self.description
        }
