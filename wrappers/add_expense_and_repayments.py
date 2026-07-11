import re
from email import message

from database.handlers import get_all_user_ids, save_expense, save_repayment
from utils.custom_errors import ExpenseSaveError, RepaymentSaveError, UserIdsFetchError
from utils.utils import (
    get_formatted_member_share,
    get_member_id_and_share,
    returnMessage,
)


def add_expense(
    payer_id: int, description: str, amount: float, listed_by: int, participants: str
):
    # get the users from db
    # check the payer and participants id to see they are in the db.
    # then make new query of adding the expense and participipants
    try:
        if amount < 0:
            return {
                "error": True,
                "message": "Amount cannot be negative.",
            }

        user_ids = get_all_user_ids()

        if payer_id not in user_ids:
            return {
                "error": True,
                "message": "The payer must be one of members added during bot initialization.",
            }

        participant_share_pair, participant_ids = get_member_id_and_share(participants)
        new_participant_share_pair = []

        # check for valid participants only.
        valid_participants = set(participant_ids).issubset(set(user_ids))

        if not valid_participants:
            return {
                "error": True,
                "message": "Enter valid participants. Only the members included when bot initialization can be participants.",
            }

        # if payer is included in participants, remove it
        if payer_id in participant_ids:
            participant_ids.remove(payer_id)
            for participant in participant_share_pair:
                if participant.get("id") != payer_id:
                    new_participant_share_pair.append(participant)
        else:
            new_participant_share_pair = participant_share_pair

        if len(participant_ids) < 1:
            return {"error": True, "message": "Enter valid participants."}

        # check if share amount is not greater than total amount
        share_amount = 0
        for participant in new_participant_share_pair:
            share_amount += participant.get("share")

        if share_amount > amount:
            return {
                "error": True,
                "message": "The total share amount of participants exceeds the total amount.",
            }

        # add the expense to the database.
        save_expense(
            (payer_id, description, listed_by, amount), new_participant_share_pair
        )

        successMessage = f"""Added the expense successfully.\nExpense saved by: <@{listed_by}>\n---------------------------------\nPaid By : <@{payer_id}>\nDescription  : {description}\nTotal Amount : {amount}\nparticipants:\n{get_formatted_member_share(participant_share_pair)}
        """

        return {"error": False, "message": successMessage}

    except UserIdsFetchError:
        return {
            "error": True,
            "message": "Failed to add expense. Couldn't get user from database.",
        }
    except ExpenseSaveError:
        return {
            "error": True,
            "message": "Failed to add expense. Couldn't save expense or participants.",
        }
    except Exception as e:
        print(e)
        return {
            "error": True,
            "message": "Failed to add expense. Unexpected error occured.",
        }


def add_repayment(sender: int, receiver: int, amount: float, note: str):
    # check if the sender and receiver are valid members.
    if amount < 0:
        return returnMessage(True, message="Amount can't be negative")

    try:
        user_ids = get_all_user_ids()
        if sender not in user_ids or receiver not in user_ids:
            return returnMessage(
                True,
                "Sender or Receiver is not a valid member when bot was initialized",
            )

        # call the databse to save the repayment
        save_repayment(sender, receiver, amount, note)

        # return success

        successMessage = f"""Saved the repayment successfully.\n-----------------------------------\n<@{sender}> paid <@{receiver}> {amount}.\nnote: {note}\n"""

        return returnMessage(False, successMessage)

    except UserIdsFetchError:
        return returnMessage(True, "Failed to save repayment. Couldn't access users.")

    except RepaymentSaveError:
        return returnMessage(
            True, "Failed to save repayment. Error occured in saving to databse."
        )

    except Exception as e:
        print(e)
        return returnMessage(
            True, "Failed to save repayment. Unexpected error occured."
        )
