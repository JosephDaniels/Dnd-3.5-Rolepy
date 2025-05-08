import os
import json

CLASS_PATH = "models/dnd_classes"

def load_class(name):
    path = os.path.join(CLASS_PATH, f"{name.lower()}.json")
    if not os.path.exists(path):
        raise ValueError(f"Unknown class: {name}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_class(name):
    try:
        load_class(name)
        return True
    except ValueError:
        return False
