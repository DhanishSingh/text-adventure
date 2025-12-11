# game_engine.py
import json
from pathlib import Path
from scene import Scene
from player import Player
from input_handler import get_choice_from_user
from story_loader import load_story

SAVE_FILENAME = "save_game.json"

class GameEngine:
    def __init__(self, story_data: dict, player: Player = None):
        self.raw_story = story_data
        self.scenes = {}
        for sid, raw in story_data.items():
            self.scenes[sid] = Scene(sid, raw)
        self.player = player or Player(self.raw_story.get("start_scene", "start") if isinstance(self.raw_story.get("start_scene"), str) else "start")
        # ensure player's current scene exists
        if self.player.current_scene not in self.scenes:
            if "start" in self.scenes:
                self.player.current_scene = "start"

    def start(self):
        print("\n== Text Adventure Engine ==\n(Type choice ID like A or 1. Type 'save' to save, 'quit' to exit.)")
        while True:
            current = self.player.current_scene
            scene = self.scenes.get(current)
            if scene is None:
                print(f"Scene '{current}' not found. Exiting.")
                break
            # show scene
            print("\n---")
            print(scene.text)
            # apply on_enter effects if exist in raw data
            raw = self.raw_story.get(current, {})
            on_enter = raw.get("on_enter", [])
            for eff in on_enter:
                self.player.apply_effect(eff)

            if scene.ending or self.player.flags.get("_END_"):
                print("\n[ THE END ]")
                # optionally show a result flag
                res = self.player.flags.get("_END_", None)
                if res:
                    print("Result:", res)
                break

            # filter choices by requirements (simple check)
            available = []
            for cid, choice in scene.choices.items():
                if self._meets_requirements(choice.requirements):
                    available.append(choice)

            if not available:
                print("\n(No available choices. Game ends.)")
                break

            # print choices numbered + id
            print()
            for i, c in enumerate(available, start=1):
                print(f"{i}) [{c.id}] {c.text}")

            valid_keys = [c.id for c in available]
            sel = get_choice_from_user("\nChoose an option: ", valid_keys)
            if sel == "quit":
                print("Goodbye.")
                break
            if sel == "save":
                self.save(SAVE_FILENAME)
                print(f"Game saved to {SAVE_FILENAME}.")
                continue

            # find selected choice object
            chosen = None
            for c in available:
                if c.id == sel:
                    chosen = c
                    break
            if not chosen:
                print("Unexpected selection error.")
                continue

            # apply effects
            for eff in chosen.effects:
                self.player.apply_effect(eff)
            # transition
            if not chosen.target:
                print("This choice has no target. Game ends.")
                break
            self.player.current_scene = chosen.target

    def _meets_requirements(self, reqs):
        """
        Very simple requirements evaluator.
        reqs is list like [{"type":"has_item","item":"lantern"}, {"type":"flag","name":"seen_cabin","value":true}]
        """
        if not reqs:
            return True
        for r in reqs:
            rt = r.get("type")
            if rt == "has_item":
                if not self.player.has_item(r.get("item")):
                    return False
            elif rt == "flag":
                name = r.get("name")
                val = r.get("value", True)
                if self.player.flags.get(name) != val:
                    return False
            elif rt == "stat_gte":
                name = r.get("name")
                amt = r.get("amount", 0)
                if self.player.stats.get(name, 0) < amt:
                    return False
            # unknown requirement -> fail-safe: allow
        return True

    def save(self, path: str):
        obj = {
            "player": self.player.to_dict()
        }
        p = Path(path)
        with p.open("w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)

    @classmethod
    def load_from_save(cls, story_data: dict, save_path: str):
        p = Path(save_path)
        if not p.exists():
            raise FileNotFoundError(f"Save file not found: {save_path}")
        with p.open(encoding="utf-8") as f:
            data = json.load(f)
        player = Player.from_dict(data.get("player", {}))
        return cls(story_data, player)
