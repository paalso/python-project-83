import requests
from bs4 import BeautifulSoup
import logging

TIMEOUT = 5


class URLChecker:
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def check(self, url: str) -> dict:
        """Checks the page and returns its parameters."""
        self.logger.info(f'Checking the page: {url}')

        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.encoding = 'utf-8'
            status_code = response.status_code

            if not response.ok:
                self.logger.warning(f'Error when requesting {url}: status code {status_code}')
                return {'status_code': status_code, 'h1': None, 'title': None, 'description': None}

            soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')

            return {
                'status_code': status_code,
                'h1': self._extract_first_h1_content(soup),
                'title': self._extract_title_content(soup),
                'description': self._extract_meta_description(soup),
            }

        except requests.RequestException as e:
            self.logger.error(f'Error when requesting {url}: {e}')
            return {'status_code': None, 'h1': None, 'title': None, 'description': None}

    def _extract_first_h1_content(self, soup):
        first_h1_tag = soup.find('h1')
        return first_h1_tag.text if first_h1_tag else None

    def _extract_title_content(self, soup):
        title_tag = soup.find('title')
        return title_tag.text if title_tag else None

    def _extract_meta_description(self, soup):
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        return meta_tag.get('content') if meta_tag else None
