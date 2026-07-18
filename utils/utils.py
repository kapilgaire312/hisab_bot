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


HELP_MESSAGE = """
# 📖 Hisab Bot Commands

### 💰 Expenses
• `/expense` - Add a shared expense.
  Format: `payer:@user description:<text> amount:<amount> participants:@userA:share,@userB:share,...`

• `/repay` - Record a repayment.
  Format: `receiver:@user amount:<amount> note:<text>`

• `/delete` - Delete a transaction by ID.

### 📊 Reports
• `/balance` - View a user's balance.
• `/history` - View a user's transaction history.
• `/history_all` - View all transactions.
• `/export_transactions` - Export all transactions as CSV.

### 🛠️ Admin
• `/initiliaze_bot` - Initialize the bot.
• `/initiliaze_bot_with_exception` - Initialize while excluding members.
• `/clear_records` - Reset transaction history.
• `/delete_database` ⚠️ - Permanently delete all data. Export a copy before running this.

💡 Type `/` in Discord to view each command's description and parameter hints.
"""
