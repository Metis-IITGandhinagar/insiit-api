from config import db_config
import psycopg2
import psycopg2.extensions


def connect() -> psycopg2.extensions.connection:
    con = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["username"],
        password=db_config["password"],
        database=db_config["database"],
    )

    return con


def disconnect(con: psycopg2.extensions.connection):
    con.close()
