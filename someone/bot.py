from __future__ import annotations

__all__: tuple[str, ...] = ("build",)

from functools import partial

import crescent
import hikari

from someone import config
from someone import plugins
from someone import listeners


def build() -> crescent.Bot:
    bot = crescent.Bot(config.TOKEN, banner=None)

    on_guild_message_create_partial = partial(
        listeners.mentions.on_guild_message_create, bot=bot
    )

    bot.subscribe(hikari.GuildMessageCreateEvent, on_guild_message_create_partial)

    for plugin in plugins.PLUGINS:
        bot.plugins.load(plugin)

    return bot
