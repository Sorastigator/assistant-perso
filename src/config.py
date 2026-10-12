"""Chargement de la config : valeurs par defaut + surcharge locale JSON."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL_CONFIG = ROOT / "config.local.json"

DEFAULTS = {
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "profile_path": "docs/profil-relay.md",
    "history_path": "data/history.json",
}


def load_config() -> dict:
    """Retourne DEFAULTS surcharge par config.local.json s'il existe."""
    config = dict(DEFAULTS)
    if LOCAL_CONFIG.exists():
        config.update(json.loads(LOCAL_CONFIG.read_text(encoding="utf-8")))
    return config


def load_profile(config: dict) -> str:
    """Lit le profil Relay (utilise comme prompt systeme)."""
    path = ROOT / config["profile_path"]
    return path.read_text(encoding="utf-8") if path.exists() else ""
