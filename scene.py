# scene.py
from typing import Dict, List, Optional

class Choice:
    def __init__(self, id: str, text: str, target: Optional[str] = None, effects: Optional[List] = None, requirements: Optional[List] = None):
        self.id = id
        self.text = text
        self.target = target
        self.effects = effects or []
        self.requirements = requirements or []

class Scene:
    def __init__(self, scene_id: str, raw: Dict):
        self.id = scene_id
        self.text = raw.get("text", "")
        self.ending = bool(raw.get("ending", False))
        # choices: dict of id -> Choice
        self.choices = {}
        raw_choices = raw.get("choices", {})
        # support two formats: dict keyed by id, or list
        if isinstance(raw_choices, dict):
            for cid, info in raw_choices.items():
                self.choices[cid] = Choice(cid, info.get("text", ""), info.get("target"), info.get("effects"), info.get("requirements"))
        elif isinstance(raw_choices, list):
            for info in raw_choices:
                cid = info.get("id")
                if cid is None:
                    continue
                self.choices[cid] = Choice(cid, info.get("text", ""), info.get("target"), info.get("effects"), info.get("requirements"))
