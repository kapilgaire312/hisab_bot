from psycopg import OperationalError

from database.handlers import get_all_users
from utils.utils import returnMessage


def get_all_users_list():
    try:
        users = get_all_users()
        message = "Members in the bot:\n"
        for user in users:
            message += f"""<@{user.get("uid")}> --> {user.get("name")}\n"""

        return returnMessage(False, message)

    except OperationalError as e:
        msg = str(e)

        if "does not exist" in msg:
            return returnMessage(True, "Bot is not initialized yet.")

        return returnMessage(True, "Failed to get the members.")

    except Exception as e:
        print(e)
        return returnMessage(True, "Failed to get initialized members.")
