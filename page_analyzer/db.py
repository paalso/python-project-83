import logging
import os

import psycopg2
from dotenv import load_dotenv
    
from page_analyzer.services.parse_url import parse_db_url

logger = logging.getLogger(__name__)

load_dotenv()

# ⚠️ WARNING: DO NOT COMMIT THIS TO A PUBLIC REPOSITORY!
SUPABASE_URL = (
    'postgresql://postgres.ibutfbecxtsbppboybvb:ckvvwKYNPKgIsLgN@'
    'aws-0-eu-north-1.pooler.supabase.com:6543/postgres'
)

DATABASE_URL = os.getenv('DATABASE_URL') or SUPABASE_URL

conn = None


def get_db():
    global conn
    if conn is None:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            db_info = parse_db_url(DATABASE_URL)
            logger.info(
                f"🛢️ Connected to DB on host: {db_info['hostname']}, "
                f"port: {db_info['port']}, db: {db_info['dbname']}, "
                f"user: {db_info['username']}"
            )
        except Exception as e:
            logger.info(f'🚫 Failed to connect to the database: {e}')
            raise
    return conn


def close_db(exception=None):
    global conn
    if conn is not None:
        conn.close()
        print('ℹ️ Database connection closed.')
        conn = None
