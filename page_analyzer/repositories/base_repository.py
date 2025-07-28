from abc import ABC, abstractmethod
from dotenv import load_dotenv
import logging
import psycopg2
from psycopg2.extras import DictCursor

from page_analyzer.db import DATABASE_URL
from page_analyzer.services.utils import parse_db_url

logger = logging.getLogger(__name__)


class BaseRepository(ABC):
    """
    Abstract base class for repositories handling database operations.
    Provides common CRUD-like methods that can be reused in specific
    repositories.
    """
    ALLOWED_FIELDS = {"id", "name", "created_at"}

    @property
    @abstractmethod
    def table_name(self):
        """
        Each repository must define its table name.
        This ensures that SQL queries are executed on the correct table.
        """
        pass

    def get_content(self):
        """
        Retrieves all records from the table.

        :return: List of dictionaries representing table rows
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    f'''SELECT * FROM {self.table_name}
                        ORDER BY created_at DESC'''
                )
                return [dict(row) for row in cur]

    def find(self, id):
        """
        Finds a record by its ID.

        :param id: The ID of the record to find
        :return: Dictionary representing the record, or None if not found
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    f'SELECT * FROM {self.table_name} WHERE id = %s', (id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def save(self, entity):
        """
        Saves an entity to the database.
        If an ID is present, updates the existing record;
        otherwise, creates a new one.

        :param entity: Dictionary representing the entity to save
        """
        if 'id' in entity and entity['id']:
            return self._update(entity)
        else:
            return self._create(entity)

    def find_by_field(self, field: str, value):
        if field not in self.ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed for search")

        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f'SELECT * FROM urls WHERE {field} = %s', (value,))
                return [dict(row) for row in cursor.fetchall()]

    def _get_connection(self):
        try:
            db_info = parse_db_url(DATABASE_URL)
            logger.info(
                f"🛢️ Connected to DB on host: {db_info['hostname']}, "
                f"port: {db_info['port']}, db: {db_info['dbname']}, "
                f"user: {db_info['username']}"
            )
            return psycopg2.connect(DATABASE_URL)
        except Exception as e:
            logger.error(f'🚫 Failed to connect to the database: {e}')
            raise

    def _update(self, entity):
        """Default update logic (can be overridden)."""
        raise NotImplementedError("Update method is not implemented.")

    def _create(self, entity):
        """Default create logic (can be overridden)."""
        raise NotImplementedError("Create method is not implemented.")
