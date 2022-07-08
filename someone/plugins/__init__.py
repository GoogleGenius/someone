from __future__ import annotations

__all__: tuple[str, ...] = ("PLUGINS",)

from pkgutil import iter_modules

PLUGINS: list[str] = [
    module.name for module in iter_modules(__path__, __package__ + ".")
]
