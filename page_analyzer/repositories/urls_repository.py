import psycopg2
from psycopg2.extras import DictCursor

from page_analyzer.repositories.base_repository import BaseRepository


class UrlsRepository(BaseRepository):
    @property
    def table_name(self):
        return 'urls'

    def _create(self, entity):
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('INSERT INTO urls (name) VALUES (%(url)s) RETURNING *', entity)
                new_record = cur.fetchone()
                self.conn.commit()
            return new_record
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Database error: {e}")
