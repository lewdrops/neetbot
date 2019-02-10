import asyncio

import discord


def msg_to_member(message):
    name = message.content[message.content.index(' ') + 1:]
    target = message.guild.get_member_named(name)
    return target


def get_role(guild, role_name):
    # print("---", isinstance(ctx, discord.message.Message))
    """returns None if server doesn't have role"""
    return discord.utils.get(guild.roles, name=role_name)


async def create_roles_if_needed(guild, *role_names):
    for name in role_names:
        if not get_role(guild, name):
            await guild.create_role(name=name)
            print(f"created role '{name}' in {guild}")


async def toggle_role_for(ctx, role_name, notices=(None, None)):
    user = ctx.message.author
    role = get_role(ctx.guild, role_name)

    if notices == (None, None):
        notrices = (f"{role_name} added to {user}", f"{role_name} removed from {user}")

    if user in role.members:
        await user.remove_roles(role)
        await ctx.send(notices[1])  # role removed notice
    else:
        await user.add_roles(role)
        await ctx.send(notices[0])  # role added notice


def after_space(S):
    return S[S.index(' ')+1:]
