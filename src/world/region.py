class Region:
    def __init__(self, name, dialect, description):
        self.name = name
        self.dialect = dialect
        self.description = description
        self.locations = []

    def add_location(self, name, loc_type, biome, notes=""):
        self.locations.append({
            "name": name,
            "type": loc_type,
            "biome": biome,
            "notes": notes
        })

    def list_locations(self):
        return self.locations

    def get_location(self, name):
        for loc in self.locations:
            if loc["name"].lower() == name.lower():
                return loc
        return "Unknown location"
