from psycopg2.extras import DictCursor

from page_analyzer.repositories.base_repository import BaseRepository


class UrlChecksRepository(BaseRepository):
    @property
    def table_name(self):
        return 'url_checks'

    def save(self, url_id):
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
