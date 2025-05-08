import re
import docx
import spacy
import random
import os
import sys
from collections import defaultdict

# Load the spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Known character_sheets and locations to help spaCy
KNOWN_CHARACTERS = {"Rynn", "Renjiro", "Nimble", "Bilgerat", "Omek"}
KNOWN_LOCATIONS = {"Dojo", "Blackwander", "Cell 13", "Wester", "Emberreach"}

EXPLICIT_KEYWORDS = [
    r"\\bslick\\b", r"\\bcum\\b", r"\\bgaping\\b", r"\\bpleasure\\b", r"\\bscent of.*?cum\\b",
    r"\\basshole\\b", r"\\bcock\\b", r"\\bwhimper\\b", r"\\bmoan\\b", r"\\bsurrender\\b", r"\\bpossession\\b",
    r"\\bsheet[s]*.*?soaked\\b", r"\\bragged breaths\\b", r"\\bpulses with.*?rhythm\\b"
]

EMOTION_KEYWORDS = [
    "fear", "shame", "pride", "desperation", "humiliation", "lust", "longing", "frustration", "obedience", "submission",
    "anger", "sadness", "hope", "pain", "ecstasy", "resignation"
]

SCENE_NAME_TEMPLATES = [
    "Whispers in {location}",
    "{character}'s Breaking Point",
    "The Lesson in {location}",
    "Fangs of {emotion}",
    "{character} and the {emotion} Within",
    "Submission at {location}",
    "Echoes of {emotion}"
]


def is_explicit(paragraph):
    for pattern in EXPLICIT_KEYWORDS:
        if re.search(pattern, paragraph, re.IGNORECASE):
            return True
    return False


def simplify_explicit(paragraph):
    lowered = paragraph.lower()
    if "cunnilingus" in lowered or "tongue" in lowered:
        return "Renjiro tied up Rynn and performed cunnilingus on her."
    if "handjob" in lowered or ("stroking" in lowered and "cock" in lowered):
        return "A character gave a handjob to another."
    if "edging" in lowered or "denial" in lowered:
        return "Renjiro teased Rynn close to climax but denied her repeatedly."
    return "[Scene summarized: sensual content removed for clarity]"


def categorize_paragraph(paragraph):
    lowered = paragraph.lower()
    if any(x in lowered for x in ["philosophy", "believes", "discipline", "lesson"]):
        return "Lore/Philosophy"
    if any(x in lowered for x in ["training", "transformation", "submission", "obedience"]):
        return "Character Development"
    if any(x in lowered for x in ["walked", "stepped", "saw", "room", "entered"]):
        return "Scene Progression"
    return "General"


def extract_entities(text):
    doc = nlp(text)
    characters = set()
    locations = set()
    verbs = set()
    emotions = set()

    for ent in doc.ents:
        if ent.label_ == "PERSON" or ent.text in KNOWN_CHARACTERS:
            characters.add(ent.text)
        elif ent.label_ in ("GPE", "LOC") or ent.text in KNOWN_LOCATIONS:
            locations.add(ent.text)

    for token in doc:
        if token.pos_ == "VERB" and not token.is_stop:
            verbs.add(token.lemma_)
        if token.lemma_.lower() in EMOTION_KEYWORDS:
            emotions.add(token.lemma_.lower())

        if token.text in KNOWN_CHARACTERS:
            characters.add(token.text)
        if token.text in KNOWN_LOCATIONS:
            locations.add(token.text)

    return characters, locations, verbs, emotions


def generate_scene_name(characters, locations, emotions):
    template = random.choice(SCENE_NAME_TEMPLATES)
    character = next(iter(characters or KNOWN_CHARACTERS), "Someone")
    location = next(iter(locations or KNOWN_LOCATIONS), "Somewhere")
    emotion = next(iter(emotions or ["Emotion"]), "Emotion")
    return template.format(character=character, location=location, emotion=emotion).strip()


def summarize_docx(path):
    doc = docx.Document(path)
    summary = []
    redacted_count = 0
    scene_counter = 1

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        characters, locations, verbs, emotions = extract_entities(text)
        character_list = ", ".join(sorted(characters)) if characters else "None"
        location_list = ", ".join(sorted(locations)) if locations else "None"
        verb_list = ", ".join(sorted(verbs)) if verbs else "None"
        emotion_list = ", ".join(sorted(emotions)) if emotions else "None"
        scene_name = generate_scene_name(characters, locations, emotions)

        if is_explicit(text):
            simplified = simplify_explicit(text)
            summary.append(
                f"### Scene {scene_counter}: {scene_name}\n**Category**: Sensual/Explicit\n**Characters**: {character_list}\n**Locations**: {location_list}\n**Emotions**: {emotion_list}\n**Summary**: {simplified}\n"
            )
            redacted_count += 1
        else:
            category = categorize_paragraph(text)
            snippet = text[:200].replace('\n', ' ')
            summary.append(
                f"### Scene {scene_counter}: {scene_name}\n**Category**: {category}\n**Characters**: {character_list}\n**Locations**: {location_list}\n**Actions**: {verb_list}\n**Emotions**: {emotion_list}\n**Summary**: {snippet}{'...' if len(text) > 200 else ''}\n"
            )

        scene_counter += 1

    return summary, redacted_count


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "Rynn Book 3 - Re-Creation.docx"
    summary, redacted = summarize_docx(filepath)

    out_name = os.path.splitext(os.path.basename(filepath))[0] + "_summary.md"

    with open(out_name, "w", encoding="utf-8") as f:
        for section in summary:
            f.write(section + "\n")

    print(f"✔ Summary complete. Simplified {redacted} explicit section(s). Output saved to {out_name}")
