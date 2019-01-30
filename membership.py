from datetime import datetime


def membership_duration(member):
    join_date = member.joined_at
    print(member, join_date)
    duration = datetime.now() - join_date
    return f'{member} - joined on - {join_date}, and has been here for {duration}'
