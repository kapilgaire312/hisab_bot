import os

from dotenv import load_dotenv
from psycopg.rows import dict_row

from database.connect import get_connection
from database.queries import (
    add_expense_query,
    add_participant_query,
    add_repayment_query,
    add_user_query,
    create_all_tables,
    create_db,
    delete_db,
    delete_expense_query,
    delete_participants_query,
    delete_repayment_entry_query,
    export_query,
    get_balance_query,
    get_history_query,
    get_users,
    update_timestamp_query,
)
from utils.custom_errors import (
    BalanceFetchError,
    DatabaseCreationFailedError,
    DeleteFailedError,
    ExpenseSaveError,
    HistoryFetchError,
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

                return users_ids
    except Exception as e:
        print("error occured", e)
        raise UserIdsFetchError() from e


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
                raise ExpenseSaveError() from e


def save_repayment(sender: int, receiver: int, amount: float, note: str):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(add_repayment_query, (sender, receiver, amount, note))

    except Exception as e:
        print(e)
        raise RepaymentSaveError() from e


def get_balance_info(member_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    get_balance_query, (member_id, member_id, member_id, member_id)
                )

                # get tuples of values as [(participant, payer, debt)]
                response = cur.fetchall()
                return response

    except Exception as e:
        print(e)
        raise BalanceFetchError() from e


def get_history(member_id: int = 0):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                query = ""
                if not member_id:
                    query = get_history_query(all=True)
                    cur.execute(query)
                else:
                    query = get_history_query(all=False)
                    cur.execute(query, (member_id, member_id, member_id, member_id))

                # responds with a list of tuple as [(type,id, payer, description, listed_by, amount, added_date, sender, receiver, note)]
                response = cur.fetchall()
                return response

    except Exception as e:
        print(e)
        raise HistoryFetchError() from e


def delete_expense_entry(eid: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(delete_participants_query, (eid,))
                cur.execute(delete_expense_query, (eid,))

            except Exception as e:
                conn.rollback()
                print(e)
                raise DeleteFailedError() from e


def delete_repayment_entry(pid: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(delete_repayment_entry_query, (pid,))

    except Exception as e:
        print(e)
        raise DeleteFailedError() from e


def clear_timestamp(initialized_by: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(update_timestamp_query, (initialized_by,))

    except Exception as e:
        print(e)
        raise e


def get_export_data():
    try:
        with get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(export_query)

                response = cur.fetchall()
                return response

    except Exception as e:
        print(e)
        raise e
