def msg_to_member(message):
    name = message.content[message.content.index(' ') + 1:]
    target = message.guild.get_member_named(name)
    return target
