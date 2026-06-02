"""
Config loader (YAML file) and configuration validation.
"""

import yaml
from pathlib import Path
from pydantic import BaseModel

#---------------------------------------
# Schema Validation
#---------------------------------------
# Pydantic to enforce schema validation, type safety
# and provide defaults for missing values

class AppConfig(BaseModel):
    name: str

class PathsConfig(BaseModel):
    logs: str
    data: str
    test: str
    rules: str
    scripts: str
    keywords: str

class APIConfig(BaseModel):
    name: str
    host: str
    port: int
    reload: bool = True

class ServerConfig(BaseModel):
    name: str
    host: str
    port: int

class DatabaseConfig(BaseModel):
    path: str
    type: str | None = "sqlite"


#---------------------------------------
# ROOT config model
#---------------------------------------
class Config(BaseModel):
    app: AppConfig
    paths: PathsConfig
    api: APIConfig
    server: ServerConfig
    database: DatabaseConfig


#---------------------------------------
# Load YAML
#---------------------------------------

# Get project root (go one level up from /config)
BASE_DIR = Path(__file__).resolve().parent.parent

# Build path to config.yaml
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

# TODO: I should implement a more robust way to handle missing
# config file, invalid YAML format, and schema validation errors,
# with proper error messages and fallbacks if necessary
# (also, path is hardcoded for now..)

def load_config():
    """ Load config YAML from file and return as a dictionary. """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)
    
        # (mapping for pydantic) **pydantic object**
        return Config(**raw_config)


# global config (simple usage)
config = load_config()
