# src/workflow_as_list/config.py
"""Configuration loading from INI files."""

import configparser
from pathlib import Path

from .models import Config

DEFAULT_CONFIG = Config(
    blacklist=[],
    whitelist=[],
    enable_whitelist=False,
    host="127.0.0.1",
    port=8080,
    config_dir="~/.config/wf",
    token_min=282,
    token_max=358,
)


def load_config(config_paths: list[Path] | None = None) -> Config:
    """Load configuration with priority:

    1. Built-in defaults
    2. ~/.config/workflow/config.ini (user)
    3. ./workflow.ini (project)
    4. CLI arguments (handled by caller)
    """
    config = configparser.ConfigParser()

    # Default values
    data = DEFAULT_CONFIG.model_dump()

    # Load from files
    paths = config_paths or [
        Path.home() / ".config" / "workflow" / "config.ini",
        Path.cwd() / "workflow.ini",
    ]

    for path in paths:
        if path.exists():
            config.read(path)

            # Parse security section
            if "security" in config:
                if "blacklist" in config["security"]:
                    data["blacklist"] = [
                        x.strip()
                        for x in config["security"]["blacklist"].split(",")
                        if x.strip()
                    ]
                if "whitelist" in config["security"]:
                    data["whitelist"] = [
                        x.strip()
                        for x in config["security"]["whitelist"].split(",")
                        if x.strip()
                    ]
                if "enable_whitelist" in config["security"]:
                    data["enable_whitelist"] = config["security"].getboolean(
                        "enable_whitelist", fallback=False
                    )

            # Parse server section
            if "server" in config:
                if "host" in config["server"]:
                    data["host"] = config["server"]["host"]
                if "port" in config["server"]:
                    data["port"] = config["server"].getint("port")

            # Parse constraints section
            if "constraints" in config:
                if "token_min" in config["constraints"]:
                    data["token_min"] = config["constraints"].getint("token_min")
                if "token_max" in config["constraints"]:
                    data["token_max"] = config["constraints"].getint("token_max")

    return Config(**data)


def ensure_config_dir(config: Config) -> Path:
    """Ensure configuration directory exists."""
    config_dir = Path(config.config_dir).expanduser()
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir
