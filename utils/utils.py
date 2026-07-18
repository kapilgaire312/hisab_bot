import re

from discord.permissions import permission_alias


def returnMessage(error: bool, message: str):
    return {"error": error, "message": message}


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

    # remove duplicates.
    unique_members = list(set(members))

    return unique_members


def get_member_id_and_share(values_string: str):
    matches = re.findall(r"<@(\d+)>\s*:\s*(\d+(?:\.\d+)?)", values_string)
    id_share_pair = []
    participant_ids = []

    for member_id, share in matches:
        try:
            int_id = int(member_id)
            float_share = float(share)

            if member_id in participant_ids:  # prevent duplicte value of same user
                continue

            id_share_pair.append({"id": int_id, "share": float_share})
            participant_ids.append(int_id)

        except ValueError:
            pass
    return (id_share_pair, participant_ids)


def get_formatted_member_share(participants):
    result = ""
    for participant in participants:
        result += f"<@{participant.get('id')}> : {participant.get('share')} \n"

    return result


def check_admin_or_mod(interaction):
    permissions = interaction.permissions

    if permissions.administrator or permissions.manage_messages:
        return True

    return False
