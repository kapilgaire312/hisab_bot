import os
import re

from dotenv import load_dotenv

from database.connect import get_connection
from database.queries import (
    add_expense_query,
    add_participant_query,
    add_repayment_query,
    add_user_query,
    create_all_tables,
    create_db,
    delete_db,
    get_balance_query,
    get_users,
)
from utils.custom_errors import (
    BalanceFetchError,
    DatabaseCreationFailedError,
    ExpenseSaveError,
    RepaymentSaveError,
    UserIdsFetchError,
    UserTableInitializeError,
)

load_dotenv()


def create_database():
    try:
        with get_connection(db_name=os.getenv("DEFAULT_DB_NAME")) as conn:
            with conn.cursor() as cursor:
                conn.autocommit = True
                cursor.execute(create_db)

        with get_connection(db_name=None) as conn:
            with conn.cursor() as cursor:
                cursor.execute(create_all_tables)
                return {"error": False}
    except Exception as e:
        print(e)
        raise DatabaseCreationFailedError() from e


def delete_database():
    try:
        with get_connection(db_name=os.getenv("DEFAULT_DB_NAME")) as conn:
            with conn.cursor() as cursor:
                conn.autocommit = True
                cursor.execute(delete_db)
                return True

    except Exception as e:
        print(e)
        return False


def initialize_users_table(
    users: list[tuple[int, str]],
):  # the users is a list of tuples containing id and name. [(id,name)]
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                for user in users:
                    print(user)
                    cursor.execute(add_user_query, user)

    except Exception as e:
        raise UserTableInitializeError() from e


def get_all_user_ids():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(get_users)
                rows = cur.fetchall()

                users_ids = []

                for row in rows:
                    users_ids.append(row[0])

                print(users_ids)
                return users_ids
    except Exception as e:
        print(e)
        raise UserIdsFetchError from e


def save_expense(
    expense_info: tuple[int, str, int, float], participant_share_list: list[dict]
):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(add_expense_query, expense_info)

                # fetch the primary key of expense.
                primary_key_eid = cur.fetchone()[0]

                for participant in participant_share_list:
                    cur.execute(
                        add_participant_query,
                        (
                            participant.get("id"),
                            primary_key_eid,
                            participant.get("share"),
                        ),
                    )

            except Exception as e:
                conn.rollback()
                print(e)
                raise ExpenseSaveError from e


def save_repayment(sender: int, receiver: int, amount: float, note: str):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(add_repayment_query, (sender, receiver, amount, note))

    except Exception as e:
        print(e)
        raise RepaymentSaveError from e


def get_balance_info(member_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(get_balance_query, (member_id, member_id))

                # get tuples of values as [(participant, payer, debt)]
                response = cur.fetchall()
                return response

    except Exception as e:
        print(e)
        raise BalanceFetchError from e
