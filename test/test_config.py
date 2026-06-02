"""
Tests the project configuration loading and structure.
"""

from config import config

def test_config_loaded():
    assert config is not None, "[ ERROR ] Config should not be None"

def test_required_sections_exist():
    required_keys = ["app", "database", "api", "paths"]
    for key in required_keys:
        assert key in config, f"[ ERROR ] Missing key in config: {key}"

def test_database_path():
    db_path = config["database"]["path"]
    assert db_path is not None, "[ ERROR ] Database path should not be None"
    assert isinstance(db_path, str), "[ ERROR ] Database path should be a string"

def test_api_settings():
    assert isinstance(config["api"]["port"], int), "[ ERROR ] API port should be an integer"
    assert isinstance(config["api"]["host"], str), "[ ERROR ] API host should be a string"

if __name__ == "__main__":
    print("Running <config> tests...")
    test_config_loaded()
    test_required_sections_exist()
    test_database_path()
    test_api_settings()
    print("✅ All config tests passed")
