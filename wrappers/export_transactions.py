from database.handlers import get_export_data
from utils.utils import returnMessage


def export_all_transactions():
    try:
        records = get_export_data()
        print(records)
        return returnMessage(False, "yo")

    except Exception as e:
        print(e)
        return returnMessage(True, "Failed to get transactions data to export.")
