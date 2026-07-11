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
    print(id_share_pair)
    return (id_share_pair, participant_ids)
