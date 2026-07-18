import csv
import io

import discord

from database.handlers import get_export_data
from utils.utils import returnMessage


def export_all_transactions():
    try:
        records = get_export_data()
        clean_records = format_records(records)
        csv_buffer = construct_csv_buffer(clean_records)

        return csv_buffer

    except Exception as e:
        print(e)
        return returnMessage(True, "Failed to get transactions data to export.")


def format_records(records):
    if not records:
        return []
    formatted_records = []

    for record in records:
        clean_record = {}
        clean_record["Id"] = record.get("id")

        clean_record["Type"] = record.get("type")

        clean_record["Added date"] = (
            record.get("added_date").date().strftime("%d %b %Y")
        )

        clean_record["Amount"] = record.get("amount")

        if record.get("type") == "expense":
            clean_record["Paid By / Sender"] = record.get("payer")

            clean_record["Description"] = record.get("description")

            clean_record["Listed By"] = record.get("listed_by")

            participants = record.get("participants")
            participants_list = ""
            for participant in participants:
                participants_list += f"{participant['name']}: {participant['share']}\n"

            clean_record["Participants / Receiver"] = participants_list

        elif record.get("type") == "repayment":
            clean_record["Paid By / Sender"] = record.get("sender")

            clean_record["Description"] = record.get("note")

            clean_record["Listed By"] = "--"

            clean_record["Participants / Receiver"] = record.get("receiver")

        elif record.get("type") == "cleared_date":
            clean_record["Paid By / Sender"] = "--"
            clean_record["Description"] = "--"

            clean_record["Listed By"] = record.get("listed_by")

            clean_record["Participants / Receiver"] = "--"
            clean_record["Amount"] = "--"

        formatted_records.append(clean_record)

    return formatted_records


def construct_csv_buffer(records):
    field_names = [
        "Id",
        "Type",
        "Added date",
        "Paid By / Sender",
        "Participants / Receiver",
        "Amount",
        "Description",
        "Listed By",
    ]

    # create a in-memory text buffer
    csv_buffer = io.StringIO()

    # initialize dictwriter of csv
    writer = csv.DictWriter(csv_buffer, fieldnames=field_names)

    # write the header
    writer.writeheader()

    # write the records
    writer.writerows(records)

    # move pointer to start of buffer
    csv_buffer.seek(0)

    return csv_buffer

    # create discord file
    discord_file = discord.File(
        fp=csv_buffer, filename="hisab_bot_transactions_report.csv"
    )

    return discord_file
