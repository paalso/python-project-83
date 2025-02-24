from psycopg2.extras import DictCursor


class UrlChecksRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('SELECT * FROM url_checks ORDER BY created_at DESC')
            return [dict(row) for row in cursor]

    def create(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                'INSERT INTO url_checks (url_id) VALUES (%s) RETURNING *',
                (url_id,)
            )
            new_record = cursor.fetchone()
            self.conn.commit()
            return new_record

    def get_by_url_id(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                '''
                SELECT
                  uc.id, uc.status_code, uc.h1, uc.title, uc.description, uc.created_at
                FROM url_checks uc
                INNER JOIN urls u
                ON u.id = uc.url_id
                WHERE uc.url_id = %s
                ORDER BY uc.created_at DESC;''',
                (url_id,)
            )
            records = cursor.fetchall()
        return records
