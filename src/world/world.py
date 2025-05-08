import json
import os

class WorldState:
    def __init__(self, world_file='world.json'):
        self.world_file = world_file
        self._load_world()

    def _load_world(self):
        if os.path.exists(self.world_file):
            with open(self.world_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "regions": {},
                "biomes": {},
                "weather": {},
                "provinces": {},
                "settlements": {},
                "points_of_interest": {}
            }

    def _save_world(self):
        with open(self.world_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_region(self, name, dialect, description):
        self.data["regions"][name] = {
            "dialect": dialect,
            "description": description
        }
        self._save_world()

    def add_province(self, name, capital=None, notes=""):
        self.data["provinces"][name] = {
            "capital": capital,
            "notes": notes,
            "settlements": []
        }
        self._save_world()

    def add_settlement(self, province_name, name, settlement_type, population=0, biome=None, features=None, notes=""):
        settlement = {
            "name": name,
            "type": settlement_type,
            "population": population,
            "biome": biome,
            "features": features or [],
            "notes": notes
        }
        self.data["settlements"][name] = settlement
        if province_name in self.data["provinces"]:
            self.data["provinces"][province_name]["settlements"].append(name)
        self._save_world()

    def add_point_of_interest(self, name, poi_type, region=None, biome=None, danger_level=0, description=""):
        self.data["points_of_interest"][name] = {
            "type": poi_type,
            "region": region,
            "biome": biome,
            "danger_level": danger_level,
            "description": description
        }
        self._save_world()

    def add_biome(self, name, features):
        self.data["biomes"][name] = features
        self._save_world()

    def set_weather(self, region_name, weather_conditions):
        self.data["weather"][region_name] = weather_conditions
        self._save_world()

    def get_region(self, name):
        return self.data["regions"].get(name, "Unknown region")

    def get_province(self, name):
        return self.data["provinces"].get(name, "Unknown province")

    def get_settlement(self, name):
        return self.data["settlements"].get(name, "Unknown settlement")

    def get_point_of_interest(self, name):
        return self.data["points_of_interest"].get(name, "Unknown point of interest")

    def get_biome(self, name):
        return self.data["biomes"].get(name, "Unknown biome")

    def get_weather(self, region_name):
        return self.data["weather"].get(region_name, "Unknown weather")
