import validators

MAX_URL_LEN = 255


def validate_url(url):
    errors = {}
    if len(url) > MAX_URL_LEN:
        errors.setdefault('url', []).append('URL превышает 255 символов')
    elif validators.url(url) is not True:
        errors.setdefault('url', []).append('Некорректный URL')
    return errors
