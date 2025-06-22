from typing import Dict, Any

class SessionContext:
    def __init__(self):
        self.memory: Dict[str, Any] = {}

    def get(self, key: str):
        return self.memory.get(key)

    def set(self, key: str, value: Any):
        self.memory[key] = value
