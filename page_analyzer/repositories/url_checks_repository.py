import psycopg2
from psycopg2.extras import DictCursor

from page_analyzer.repositories.base_repository import BaseRepository


class UrlChecksRepository(BaseRepository):
    @property
    def table_name(self):
        return 'url_checks'

    def get_by_url_id(self, url_id):
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('''
                    SELECT
                      uc.id, uc.status_code, uc.h1,
                      uc.title, uc.description, uc.created_at
                    FROM url_checks uc
                    INNER JOIN urls u
                    ON u.id = uc.url_id
                    WHERE uc.url_id = %s
                    ORDER BY uc.created_at DESC;''',
                    (url_id,)
                )
                records = cur.fetchall()
            return records

    def _create(self, entity):
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute('''
                        INSERT INTO url_checks (url_id, status_code, h1, title, description)
                        VALUES (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, %(description)s)
                        RETURNING *''', entity)
                    new_record = cur.fetchone()
            return new_record
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
