import yaml
import os

def load_config(filename: str) -> dict:
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

class Settings:
    def __init__(self):
        self.security = load_config('security.yaml')
        self.database = load_config('database.yaml')
        
settings = Settings()
