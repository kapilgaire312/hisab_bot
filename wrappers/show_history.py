from database.handlers import get_history_all
from utils.custom_errors import HistoryFetchError
from utils.utils import returnMessage


def show_history_all():
    try:
        # responds with a list of tuple as [(type,id, payer, description, listed_by, amount, added_date, sender, receiver, note)]
        rows = get_history_all()

        formatted_msg = format_return_message(rows)
        return returnMessage(False, formatted_msg)

    except HistoryFetchError as e:
        print(e)
        return returnMessage(True, "Failed to fetch history from database.")

    except Exception as e:
        print(e)
        return returnMessage(True, "Failed to fetch history. Unexpected error occured.")


def format_return_message(all_records):
    message = "Transaction History:\n"
    line = "-----------------------------------------\n"
    message += line

    # responds with a list of tuple as [(type,id, payer, description, listed_by, amount, added_date, sender, receiver, note)]

    for record in all_records:
        if record[0] == "expense":
            message += (
                f"**Expense #{record[1]}**\n"
                f"<t:{int(record[6].timestamp())}:d>\n"
                f"**{record[3]}**\n"
                f"Paid By: <@{record[2]}>\n"
                f"Amount: {record[5]}\n"
                f"Listed By: <@{record[4]}>\n\n"
            )

        elif record[0] == "repayment":
            message += (
                f"**Payment #{record[1]}**\n"
                f"<t:{int(record[6].timestamp())}:d>\n"
                f"<@{record[7]}> Paid <@{record[8]}>\n"
                f"Amount: {record[5]}\n"
                f"Note: {record[9]}\n\n"
            )
        message += line

    return message
