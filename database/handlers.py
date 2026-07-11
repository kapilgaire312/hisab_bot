import os
from email import message

from dotenv import load_dotenv
from psycopg.errors import DuplicateDatabase

from database.commands import add_user, create_all_tables, create_db, db_name, delete_db
from database.connect import get_connection
from utils.custom_errors import DatabaseCreationFailedError, UserTableInitializeError

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
        with get_connection(db_name=None) as conn:
            with conn.cursor() as cursor:
                for user in users:
                    print(user)
                    cursor.execute(add_user, user)

    except Exception as e:
        raise UserTableInitializeError() from e
