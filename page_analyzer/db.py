import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


def get_db():
    return conn


def close_db(exception):
    global conn
    if conn is not None:
        conn.close()
        conn = None
