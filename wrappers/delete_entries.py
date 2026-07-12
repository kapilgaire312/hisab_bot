import re

from database.handlers import delete_expense_entry, delete_repayment_entry
from utils.custom_errors import DeleteFailedError
from utils.utils import returnMessage


def delete_entry(id: str):
    try:
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
            delete_repayment_entry(rid=int_id)

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
