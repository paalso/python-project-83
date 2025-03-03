import psycopg2
from psycopg2.extras import DictCursor

from page_analyzer.repositories.base_repository import BaseRepository


class UrlsRepository(BaseRepository):
    @property
    def table_name(self):
        return 'urls'

    def get_urls_with_last_check(self):
        """
        Retrieves all URLs with their last check time and status code.

        :return: List of dictionaries representing enriched URL records.
        """
        with self.conn:
            with self.conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                    SELECT DISTINCT ON (u.id)
                        u.id,
                        u.name,
                        uc.created_at AS url_last_check_time,
                        uc.status_code
                    FROM urls u
                    LEFT JOIN url_checks uc ON u.id = uc.url_id
                    ORDER BY u.id DESC, uc.created_at DESC NULLS LAST
                """)
                return [dict(row) for row in cur]

    def _create(self, entity):
        try:
            with self.conn:
                with self.conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute('INSERT INTO urls (name) VALUES (%(url)s) RETURNING *', entity)
                    new_record = cur.fetchone()
            return new_record
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
