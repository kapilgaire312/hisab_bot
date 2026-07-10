import psycopg
from psycopg import OperationalError

from database import connect

try:
    with connect.get_connection() as conn:
        with conn.cursor() as cur:
            print("yay")


except OperationalError as e:
    print("failed")
    msg = str(e)

    if "does not exist" in msg:
        print("Database doesnt exist")
