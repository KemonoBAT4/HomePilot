import json
import os
import uuid
from pathlib import Path

CONFIG_DIR : Path = Path(os.path.expanduser("~")) / ".homepilot"
CONFIG_FILE: Path = CONFIG_DIR / "config.json"

DEFAULT_CONFIG: dict = {
    "device_id"  : None,
    "paired"     : False,
    "token"      : None,
    "server_url" : None,
}

def load_config() -> dict:
    """
    #### DESCRIPTION:
    Loads the configuration from the file or returns the default one

    #### PARAMETERS:
    No parameters

    #### RETURNS:
    The configuration file
    """

    CONFIG_DIR.mkdir(exist_ok=True)

    if (not CONFIG_FILE.exists()):
        cfg = dict(DEFAULT_CONFIG)
        cfg["device_id"] = str(uuid.uuid4())
        save_config(cfg)
        return cfg
    # #endif

    with (open(CONFIG_FILE, "r") as f):
        return json.load(f)
    # #endwith
# #enddef load_config

def save_config(cfg: dict) -> None:
    """
    #### DESCRIPTION:
    Saves the configuration to the file

    #### PARAMETERS:
    - `cfg` (`dict`): The configuration to save

    #### RETURNS:
    No return
    """

    CONFIG_DIR.mkdir(exist_ok=True)

    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    # #endwith
# #enddef save_config

def reset_pairing() -> None:
    """
    #### DESCRIPTION:
    Resets the pairing

    #### PARAMETERS:
    No parameters

    #### RETURNS:
    No return
    """

    cfg = load_config()
    cfg["paired"]     = False
    cfg["token"]      = None
    cfg["server_url"] = None

    save_config(cfg)
# #enddef reset_pairing
