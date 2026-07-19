import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


DB_URL = os.getenv("DB_CONNECTION_STRING")


def get_connection(db_name=None):
    if db_name:  # when there is not database, so we default to postgres database that it creates.
        db_removed_list = DB_URL.split("/")[:-1]
        url = "/".join(db_removed_list) + "/" + db_name
        print(url)
        return psycopg.connect(url)

    return psycopg.connect(DB_URL)
