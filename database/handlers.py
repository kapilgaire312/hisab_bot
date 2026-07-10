import os

from dotenv import load_dotenv
from psycopg.errors import DuplicateDatabase

from database.commands import create_all_tables, create_db, db_name, delete_db
from database.connect import get_connection

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
                return True
    except DuplicateDatabase:
        print("Database already exists, skipping.")
    except Exception as e:
        print(type(e))
        return False


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
