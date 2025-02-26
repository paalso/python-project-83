from flask import (
    Blueprint,
    flash,
    get_flashed_messages,
    render_template,
    request
)
from page_analyzer.db import get_db
from page_analyzer.repositories import UrlsRepository, UrlChecksRepository
from page_analyzer.validator import validate_url
from urllib.parse import urlparse

FLASH_MESSAGES = {
    'url_exists': ('Страница уже существует', 'warning'),
    'url_added': ('Страница успешно добавлена', 'success'),
    'url_checked': ('Страница успешно проверена', 'success'),
}


def flash_errors(errors, key):
    for error in errors.get(key, []):
        flash(error, 'error')


def normalize_url(url):
    parsed_url = urlparse(url)
    url_scheme = parsed_url.scheme
    url_host = parsed_url.hostname

    if not url_scheme or not url_host:
        return None

    return f"{url_scheme}://{url_host}"


routes = Blueprint('routes', __name__)
conn = get_db()
urls_repo = UrlsRepository(conn)
urls_checks_repo = UrlChecksRepository(conn)


@routes.route('/')
@routes.route('/index')
def index():
    return render_template('index.html')


@routes.route('/urls')
def urls():
    urls = urls_repo.get_content()
    return render_template('urls.html', urls=urls)


@routes.route('/urls/<int:id>')
def show_url(id):
    url_info = urls_repo.find(id)
    if not url_info:
        return render_template('not_found_url.html'), 404

    url_checks = urls_checks_repo.get_by_url_id(id)
    return render_template(
        'url.html',
        url_info=url_info,
        url_checks=url_checks
    )


@routes.post('/urls')
def urls_post():
    data = _get_form_data()
    url = data.get('url').strip()
    errors = validate_url(url)
    if errors:
        return handle_validation_errors(errors, url)

    normalized_url = normalize_url(url)
    existing_records = urls_repo.find_by_field('name', normalized_url)

    if existing_records:
        existing_record = existing_records[0]
        flash(*FLASH_MESSAGES['url_exists'])
        return _render_url_page(existing_record)

    data['url'] = normalized_url
    created_record = urls_repo.save(data)
    flash(*FLASH_MESSAGES['url_added'])

    return _render_url_page(created_record)


@routes.post('/urls/<int:id>/checks')
def create_url_check(id):
    urls_checks_repo.save(id)
    url_info = urls_repo.find(id)
    url_checks = urls_checks_repo.get_by_url_id(id)
    flash(*FLASH_MESSAGES['url_checked'])
    return render_template(
        'url.html',
        url_info=url_info,
        url_checks=url_checks,
        messages = get_flashed_messages(with_categories=True)
    )


# TODO: remove after debugging
@routes.route('/conn')
def get_conn():
    return str(id(conn))


def _get_form_data():
    return request.form.to_dict()


def _render_url_page(url_info):
    return render_template(
        'url.html',
        url_info=url_info,
        messages=get_flashed_messages(with_categories=True)
    )


def handle_validation_errors(errors, url):
    flash_errors(errors, 'url')
    return render_template(
        'index.html',
        url=url,
        messages=get_flashed_messages(with_categories=True)
    )
