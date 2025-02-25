from psycopg2.extras import DictCursor

from page_analyzer.repositories.base_repository import BaseRepository


class UrlsRepository(BaseRepository):
    @property
    def table_name(self):
        return 'urls'

    def save(self, url):
        existing = self._find_by_field('name', url)

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
