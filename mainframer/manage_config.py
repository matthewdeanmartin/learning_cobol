import tomllib
from pathlib import Path

import tomli_w

DEFAULT_INSTALL_DIR = Path.home() / ".cobols"


def load_config(path: Path) -> dict:
    """Load the configuration from the framer.toml file.

    Returns:
        dict: The configuration data as a dictionary.
    """
    if path.exists():
        with path.open("rb") as f:
            return tomllib.load(f)
    return {}


def save_config(path: Path, config: dict) -> None:
    """Save the configuration to the framer.toml file.

    Args:
        path (Path): The path to the configuration file.
        config (dict): The configuration data to save.
    """
    with path.open("wb") as f:
        tomli_w.dump(config, f)
