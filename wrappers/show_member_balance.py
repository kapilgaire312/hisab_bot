from database.handlers import get_all_user_ids, get_balance_info
from utils.custom_errors import BalanceFetchError, UserIdsFetchError
from utils.utils import returnMessage


def show_balance(member_id: int):
    # join the expense_repayments table with the expense table
    # and retirieve the tuples which has this member_id as payer or uid from participant table.
    try:
        user_ids = get_all_user_ids()

        if member_id not in user_ids:
            return returnMessage(
                True, "Given member was not registered when bot was initialized."
            )

        # get tuples of values as [(participant, payer, debt)]
        rows = get_balance_info(member_id=member_id)

        # initialize a dict and record how much member owes other.
        # if final value is positive, he owes other, else they owe him.
        # so we only need to store the other party in a expense.
        member_balance = {}

        # first compare the member id to participant(first value of tuple),
        # if same it means user owes the other party(payer,second value of tuple)
        # else, the payer is the user and other party owes him.
        # we will only record the other party,
        # add the balance if member is participant
        # subtract balance if member is payer.

        for row in rows:
            participant, payer, amount = row

            if participant == member_id:
                member_balance[f"{payer}"] = member_balance.get(f"{payer}", 0) + amount

            elif payer == member_id:
                member_balance[f"{participant}"] = (
                    member_balance.get(f"{participant}", 0) - amount
                )

        balance_info = print_balance_info(
            member_balance=member_balance, member_id=member_id
        )

        return returnMessage(False, balance_info)

    except UserIdsFetchError:
        return returnMessage(
            True, "Failed to get the balance of user. User ids couldn't be fetched"
        )

    except BalanceFetchError:
        return returnMessage(True, "Failed to get the balance of user. Database error.")

    except Exception as e:
        print(e)
        return returnMessage(
            True, "Failed to get the balance of user. Unexpected error occured."
        )


def print_balance_info(member_balance: dict, member_id: int):
    message = f"""Balance for <@{member_id}>\n------------------------------"""

    if not member_balance:
        message += "\n\nMember owes:\n\tNoone\n\nPeople owing Member:\n\tNoone"
        return message

    user_owes = []
    other_owes = []

    for member, amount in member_balance.items():
        if amount > 0:
            user_owes.append({"member": member, "amount": amount})

        elif amount < 0:
            other_owes.append({"member": member, "amount": abs(amount)})

    message += "\n\nMember owes:"

    if not user_owes:
        message += "\n\tNoone"

    else:
        for item in user_owes:
            message += f"\n\t<@{item['member']}> : {item['amount']}"

    message += "\n\nPeople owing Member:"
    if not other_owes:
        message += "\n\tNoone"

    else:
        for item in other_owes:
            message += f"\n\t<@{item['member']}> : {item['amount']}"

    return message
