from psycopg2.extras import DictCursor


class Repository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('SELECT * FROM urls ORDER BY created_at DESC')
            return [dict(row) for row in cursor]

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('SELECT * FROM urls WHERE id = %s', (id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def find_by_field(self, field: str, value):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            query = f'SELECT * FROM urls WHERE {field} = %s'
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows] if rows else None

    def create(self, url):
        existing = self.find_by_field('name', url)

        if existing:
            return

        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                'INSERT INTO urls (name) VALUES (%s) RETURNING *',
                (url,)
            )
            new_record = cursor.fetchone()
            self.conn.commit()
            return new_record
