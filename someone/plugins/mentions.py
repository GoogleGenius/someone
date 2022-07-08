from __future__ import annotations

__all__: tuple[str, ...] = ()

import random
from contextlib import suppress

import crescent
import hikari
from crescent.ext import docstrings

plugin = crescent.Plugin()


@plugin.include
@docstrings.parse_doc
@crescent.command
async def bing_bong(ctx: crescent.Context, message: str) -> None:
    """Mention a random user along with a specified message

    Parameters
    ----------
    message: str
        Message to send; mention the bot to inject a random user
    """
    await ctx.defer(ephemeral=True)

    if ctx.guild_id is None:
        await ctx.respond("This command can only be used within a guild!")
        return

    assert ctx.member is not None

    iterator = ctx.app.rest.fetch_members(ctx.guild_id).filter(lambda m: not m.is_bot)
    members: list[hikari.Member] = []

    async for m in iterator:
        members.append(m)

    member = random.choice(members)

    while member == ctx.member:
        member = random.choice(members)

    webhook = await ctx.app.rest.create_webhook(
        ctx.channel_id,
        ctx.member.display_name,
        avatar=ctx.member.avatar_url or ctx.member.default_avatar_url,
    )

    own_user = ctx.app.get_me() or await ctx.app.rest.fetch_my_user()

    with suppress(hikari.NotFoundError):
        if own_user.mention not in message:
            await webhook.execute(f"{member.mention}\n{message}")
        else:
            await webhook.execute(message.replace(own_user.mention, member.mention))
        await webhook.delete()

    await ctx.respond("✅ Success!")
