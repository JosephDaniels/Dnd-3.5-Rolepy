from datetime import datetime
from src.main_bot import active_chars

# Events mapping: key -> (stat_name, delta, journal_message)
EVENT_MAP = {
    "quest_success": ("happiness", +20, "celebrated a grand victory!"),
    "companion_falls": ("sadness", +30, "grieved the loss of a friend."),
    "insulted": ("anger", +15, "grew angry at an insult."),
    "narrow_escape": ("fear", +25, "survived a hair-raising encounter."),
    # Extend with more game events...
}


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def trigger_event(user_id: str, event_key: str) -> bool:
    """
    Apply a game event to the specified user's character:
    - Adjusts the corresponding mental stat by delta.
    - Records a journal entry with timestamp.
    - Saves the character JSON.

    Returns True if event applied, False otherwise.
    """
    if event_key not in EVENT_MAP:
        return False

    stat, delta, message = EVENT_MAP[event_key]
    char = active_chars.get(user_id)
    if not char:
        return False

    # Adjust mental status
    current_val = getattr(char.mental_status, stat, 0.0)
    new_val = clamp(current_val + delta, 0.0, 100.0)
    setattr(char.mental_status, stat, new_val)

    # Append journal entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"[{timestamp}] {char.name} {message}"
    if not hasattr(char, 'journal'):
        char.journal = []
    char.journal.append(entry)

    # Save to JSON
    char.save_to_json()
    return True


if __name__ == "__main__":
    # Simple CLI for testing
    import argparse

    parser = argparse.ArgumentParser(description="Trigger a game event for debugging.")
    parser.add_argument("user_id", help="Discord user ID of the character owner")
    parser.add_argument("event_key", help="Event key to trigger")
    args = parser.parse_args()

    success = trigger_event(args.user_id, args.event_key)
    if success:
        print(f"Event '{args.event_key}' applied to user {args.user_id}.")
    else:
        print(f"Failed to apply event '{args.event_key}'. Check user ID or event key.")
