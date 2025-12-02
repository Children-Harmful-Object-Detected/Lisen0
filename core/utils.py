import yaml
from pathlib import Path

def load_config(config_path: str) -> dict:
    """Loads a YAML config file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def resolve_path(base_path_str: str, relative_path_str: str) -> Path:
    """Resolves a relative path with respect to a base path."""
    base_path = Path(base_path_str).parent
    return (base_path / relative_path_str).resolve()
