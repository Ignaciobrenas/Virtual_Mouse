import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULT_CONFIG = {
    "language": "es",
    "smoothening": 4,
    "margin": 50,
    "click_threshold": 35,
    "right_click_threshold": 35,
    "scroll_speed": 20,
    "sound_enabled": True,
    "two_hands_mode": True,
    "tony_stark_mode": True,
    "camera_index": 0
}


def load_config():
    """Carga la configuración del usuario desde disco o devuelve la predeterminada."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                return config
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Guarda la configuración actual en disco."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception:
        return False
