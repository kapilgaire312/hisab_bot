import re

from database.handlers import (
    clear_timestamp,
    delete_database,
    delete_expense_entry,
    delete_repayment_entry,
)
from utils.custom_errors import DeleteFailedError
from utils.utils import check_admin_or_mod, check_user_initialized, returnMessage


def delete_enitre_db(interaction):
    is_mod = check_admin_or_mod(interaction)

    if not is_mod:
        return returnMessage(
            True, "Only an admin or a moderator can delete the database."
        )

    try:
        delete_database()
        return returnMessage(False, "The entire database was deleted successfully.")

    except Exception as e:
        print(e)

        return returnMessage(True, "Failed to delete the database.")


def delete_entry(id: str, user_id):
    try:
        is_initialized = check_user_initialized(user_id=user_id)

        if not is_initialized:
            return returnMessage(True, "Failed to clear database. Not allowed!")

        clean_id = id.strip()

        if clean_id.startswith("#"):
            clean_id = clean_id[1:]

        pattern = r"^[ep]\d+$"

        if not re.fullmatch(pattern, clean_id):
            return returnMessage(True, "Enter a valid id.")

        type = clean_id[0]

        int_id = int(clean_id[1:])

        if type == "e":
            delete_expense_entry(eid=int_id)

        elif type == "p":
            delete_repayment_entry(pid=int_id)

        return returnMessage(
            False,
            f"{'Expense' if type == 'e' else 'Repayment'} with id {clean_id} deleted successfully.",
        )

    except DeleteFailedError as e:
        print(e)
        return returnMessage(True, "Failed to delete entry from database.")
    except Exception as e:
        print(e)
        return returnMessage(True, "Failed to delete entry. Unexpected error occured.")


def clear_database_records(user_id):  # updates teh timestamp to now()
    try:
        is_initialized = check_user_initialized(user_id=user_id)

        if not is_initialized:
            return returnMessage(True, "Failed to clear database. Not allowed!")
        clear_timestamp(initialized_by=user_id)
        return returnMessage(False, "The database was cleared successfully.")

    except Exception:
        return returnMessage(True, "Failed to clear the database.")
