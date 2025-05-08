import re

def name_to_filename(name: str) -> str:
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', name.strip())
    slug = re.sub(r'_+', '_', slug).strip('_').lower()
    return f"{slug}.json"

def filename_to_name(filename: str) -> str:
    base = filename.replace(".json", "")
    parts = base.split('_')
    return ' '.join(word.capitalize() for word in parts)
