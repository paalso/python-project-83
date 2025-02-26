import requests

TIMEOUT = 5


def check_url(url):
    """Executes an HTTP request to the URL, checks it and returns
       the result of the validation."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return {
            'status_code': response.status_code,
        }
    except requests.RequestException:
        return {
            'status_code': None,
        }
