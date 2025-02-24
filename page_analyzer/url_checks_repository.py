from psycopg2.extras import DictCursor


class UrlChecksRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('SELECT * FROM url_checks ORDER BY created_at DESC')
            return [dict(row) for row in cursor]
