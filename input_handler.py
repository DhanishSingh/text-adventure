# input_handler.py
def get_choice_from_user(prompt: str, valid_keys: list):
    """
    valid_keys: list of strings (choice ids)
    returns: the chosen key, or commands: "save", "quit"
    """
    valid_set = set(valid_keys)
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Please type a choice.")
            continue
        lower = raw.lower()
        if lower in ("q", "quit", "exit"):
            return "quit"
        if lower in ("s", "save"):
            return "save"
        # exact match (A, B, 1, etc.)
        if raw in valid_set:
            return raw
        # allow selecting by number if choices numbered 1..n
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(valid_keys):
                return valid_keys[idx]
        print("Invalid choice. Try again. (or type 'save' or 'quit')")
