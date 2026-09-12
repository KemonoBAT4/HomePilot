import json
import os
import uuid
from pathlib import Path

CONFIG_DIR = Path(os.path.expanduser("~")) / ".homepilot"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "device_id": None,
    "paired": False,
    "token": None,
    "server_url": None,
}


def load_config() -> dict:
    CONFIG_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        cfg = dict(DEFAULT_CONFIG)
        cfg["device_id"] = str(uuid.uuid4())
        save_config(cfg)
        return cfg
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(cfg: dict) -> None:
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def reset_pairing() -> None:
    cfg = load_config()
    cfg["paired"] = False
    cfg["token"] = None
    cfg["server_url"] = None
    save_config(cfg)
