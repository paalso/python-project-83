from psycopg2.extras import DictCursor


class Repository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM urls ORDER BY created_at DESC')
            return [dict(row) for row in cur]
