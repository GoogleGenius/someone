from __future__ import annotations

__all__: tuple[str, ...] = ("on_guild_message_create",)

import random
from contextlib import suppress

import hikari
import crescent


async def on_guild_message_create(
    event: hikari.GuildMessageCreateEvent, bot: crescent.Bot
) -> None:
    own_user = bot.get_me() or await bot.rest.fetch_my_user()

    if not event.content or not event.member or own_user.mention not in event.content:
        return

    await bot.rest.trigger_typing(event.channel_id)

    iterator = bot.rest.fetch_members(event.guild_id).filter(lambda m: not m.is_bot)
    members: list[hikari.Member] = []

    async for m in iterator:
        members.append(m)

    member = random.choice(members)

    while member == event.member:
        member = random.choice(members)

    webhook = await bot.rest.create_webhook(
        event.channel_id,
        event.member.display_name,
        avatar=event.member.avatar_url or event.member.default_avatar_url,
    )

    with suppress(hikari.NotFoundError):
        await webhook.execute(event.content.replace(own_user.mention, member.mention))
        await webhook.delete()

        await event.message.delete()
