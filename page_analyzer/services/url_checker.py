import requests
from bs4 import BeautifulSoup

TIMEOUT = 5


class URLChecker:
    def __init__(self, url: str):
        self.url = url
        self.status_code = None
        self.soup = None

        self._fetch_page()

    def check(self) -> dict:
        return {
            'status_code': self.status_code,
            'h1': self._extract_first_h1_content(),
            'title': self._extract_title_content(),
            'description': self._extract_meta_description(),
        }

    def _fetch_page(self):
        try:
            response = requests.get(self.url, timeout=TIMEOUT)
            self.status_code = response.status_code

            if response.ok:
                self.soup = BeautifulSoup(response.text, "html.parser")

        except requests.RequestException:
            self.status_code = None

    def _get_html(self):
        return self.url

    def _get_response_status(self):
        try:
            self.response = requests.get(self.url, timeout=TIMEOUT)
            self.status_code = self.response.status_code
            return self.status_code
        except requests.RequestException:
            return

    def _extract_first_h1_content(self):
        if not self.soup:
            return
        first_h1_tag = self.soup.find('h1')
        return first_h1_tag.text if first_h1_tag else None

    def _extract_title_content(self):
        if not self.soup:
            return
        title_tag = self.soup.find('title')
        return title_tag.text if title_tag else None

    def _extract_meta_description(self):
        if not self.soup:
            return
        meta_tag = self.soup.find("meta", attrs={"name": "description"})
        return meta_tag.get('content') if meta_tag else None
