import json
from pathlib import Path

class StoryLoadError(Exception):
    pass

def load_story(path):
    p = Path(path)
    if not p.exists():
        raise StoryLoadError(f"Story file not found: {path}")
    with p.open(encoding="utf-8") as f:
        data = json.load(f)
    # Basic validation: must contain 'start' scene
    if "start" not in data:
        raise StoryLoadError("Story must contain a 'start' scene id.")
    return data
