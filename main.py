# main.py
import sys
from story_loader import load_story, StoryLoadError
from game_engine import GameEngine

def main(argv):
    if len(argv) < 2:
        print("Usage: python main.py <story.json> [--load save.json]")
        return
    story_path = argv[1]
    load_path = None
    if len(argv) >= 3 and argv[2] in ("--load", "-l"):
        if len(argv) >= 4:
            load_path = argv[3]
        else:
            print("Usage for load: python main.py story.json --load save.json")
            return

    try:
        story = load_story(story_path)
    except StoryLoadError as e:
        print("Error loading story:", e)
        return

    try:
        if load_path:
            engine = GameEngine.load_from_save(story, load_path)
        else:
            engine = GameEngine(story)
        engine.start()
    except Exception as e:
        print("Runtime error:", e)

if __name__ == "__main__":
    main(sys.argv)
# This is my first commit update
