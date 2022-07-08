from __future__ import annotations

__all__: tuple[str, ...] = ("TOKEN",)

import tomli

with open("config.toml", "rb") as f:
    config = tomli.load(f)

TOKEN: str = config["TOKEN"]
