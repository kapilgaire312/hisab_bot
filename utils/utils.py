import re


def get_member_id_from_string(members_str: str):
    if not members_str.strip():
        return []

    member_ids = re.findall(r"<@(\d+)>", members_str)

    members = []

    for member_id in member_ids:
        try:
            int_id = int(member_id)
            members.append(int_id)

        except ValueError:
            pass

    return members
