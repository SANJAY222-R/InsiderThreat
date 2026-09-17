import os
from typing import Any, Dict
import yaml

def load_config(filename: str) -> Dict[str, Any]:
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}

class Settings:
    def __init__(self) -> None:
        self.security = load_config('security.yaml')
        self.database = load_config('database.yaml')

settings = Settings()
