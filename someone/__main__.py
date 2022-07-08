from __future__ import annotations

import os

from someone import bot

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot.build().run()
