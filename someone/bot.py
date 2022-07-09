from __future__ import annotations

__all__: tuple[str, ...] = ("build",)

from functools import partial

import crescent
import hikari

from someone import config
from someone import plugins
from someone import listeners


class RoboApp(crescent.Bot):
    def __init__(self, token: str, *, intents: hikari.Intents) -> None:
        super().__init__(token, banner=None, intents=intents)

    async def on_crescent_command_error(self, exc: Exception, ctx: crescent.Context, was_handled: bool) -> None:
        if was_handled:
            return

        await ctx.respond("( ! ) This interaction failed", ephemeral=True)
        raise exc


def build() -> RoboApp:
    bot = RoboApp(config.TOKEN, intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.GUILD_MEMBERS)

    on_guild_message_create_partial = partial(listeners.mentions.on_guild_message_create, bot=bot)
    bot.subscribe(hikari.GuildMessageCreateEvent, on_guild_message_create_partial)

    for plugin in plugins.PLUGINS:
        bot.plugins.load(plugin)

    return bot
