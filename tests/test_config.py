from src.config import DEFAULTS, load_config


def test_load_config_has_defaults():
    config = load_config()
    for key in DEFAULTS:
        assert key in config
