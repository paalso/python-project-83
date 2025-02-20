import psycopg2
from flask import g
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_db():
    if 'conn' not in g:
        g.conn = psycopg2.connect(DATABASE_URL)
    return g.conn


def close_db(exception):
    conn = g.pop('conn', None)
    if conn is not None:
        conn.close()
