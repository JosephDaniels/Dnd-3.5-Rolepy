class Province:
    def __init__(self, name, capital=None, notes=""):
        self.name = name
        self.capital = capital
        self.notes = notes
        self.settlements = []

    def add_settlement(self, name, settlement_type, population=0, notes=""):
        self.settlements.append({
            "name": name,
            "type": settlement_type,
            "population": population,
            "notes": notes
        })

    def list_settlements(self):
        return self.settlements

    def get_settlement(self, name):
        for s in self.settlements:
            if s["name"].lower() == name.lower():
                return s
        return "Unknown settlement"