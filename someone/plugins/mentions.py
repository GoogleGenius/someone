from __future__ import annotations

__all__: tuple[str, ...] = ()

import random

import crescent
import hikari
from crescent.ext import docstrings

plugin = crescent.Plugin()


@plugin.include
@docstrings.parse_doc
@crescent.command
async def someone(ctx: crescent.Context, message: str) -> None:
    """Mention a random user along with a specified message

    Parameters
    ----------
    message: str
        Message to send; mention the bot to inject a random user
    """
    await ctx.defer(ephemeral=True)

    if ctx.guild_id is None:
        await ctx.respond(
            hikari.Embed(description="This command is only available within guilds!")
        )
        return

    assert ctx.member is not None

    members = list(ctx.app.cache.get_members_view_for_guild(ctx.guild_id).values())

    for m in members:
        if m == ctx.member or m.is_bot:
            members.remove(m)

    member = random.choice(members)

    webhook = await ctx.app.rest.create_webhook(
        ctx.channel_id,
        ctx.member.display_name,
        avatar=ctx.member.avatar_url or ctx.member.default_avatar_url,
    )

    own_user = ctx.app.get_me() or await ctx.app.rest.fetch_my_user()
    own_user_mention = f"<@!{own_user.id}>"

    if own_user_mention not in message:
        await webhook.execute(f"{own_user_mention} {message}")
    else:
        await webhook.execute(message.replace(own_user_mention, member.mention))
    await webhook.delete()

    await ctx.respond("✅ Success!")
