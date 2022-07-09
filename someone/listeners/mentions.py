from __future__ import annotations

__all__: tuple[str, ...] = ("on_guild_message_create",)

import random

import hikari
import crescent


async def on_guild_message_create(event: hikari.GuildMessageCreateEvent, bot: crescent.Bot) -> None:
    own_user = bot.get_me() or await bot.rest.fetch_my_user()

    if not event.content or not event.member or own_user.mention not in event.content:
        return

    await bot.rest.trigger_typing(event.channel_id)

    members = list(bot.cache.get_members_view_for_guild(event.guild_id).values())

    for m in members:
        if m == event.member or m.is_bot:
            members.remove(m)

    member = random.choice(members)

    webhook = await bot.rest.create_webhook(
        event.channel_id,
        event.member.display_name,
        avatar=event.member.avatar_url or event.member.default_avatar_url,
    )

    await webhook.execute(event.content.replace(own_user.mention, member.mention))
    await webhook.delete()

    await event.message.delete()
