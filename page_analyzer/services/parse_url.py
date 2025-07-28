from urllib.parse import urlparse


def parse_db_url(database_url):
    """Parses DATABASE_URL and returns safe info:
    hostname, port, dbname, username (no password)."""
    parsed = urlparse(database_url)
    return {
        'hostname': parsed.hostname,
        'port': parsed.port,
        'dbname': parsed.path.lstrip('/'),
        'username': parsed.username,
    }
