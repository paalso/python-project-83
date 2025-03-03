from flask import (
    Blueprint,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for
)
from urllib.parse import urlparse

from page_analyzer.db import get_db
from page_analyzer.repositories import UrlsRepository, UrlChecksRepository
from page_analyzer.validator import validate_url
from page_analyzer.services.url_checker import URLChecker
import requests

FLASH_MESSAGES = {
    'url_exists': ('Страница уже существует', 'warning'),
    'url_added': ('Страница успешно добавлена', 'success'),
    'url_checked': ('Страница успешно проверена', 'success'),
    'url_check_error': ('Произошла ошибка при проверке', 'error'),
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
def urls_index():
    urls_with_last_check = urls_repo.get_urls_with_last_check()
    return render_template('urls.html', urls=urls_with_last_check)


@routes.route('/urls/<int:id>')
def urls_show(id):
    url_info = urls_repo.find(id)
    if not url_info:
        return render_template('not_found_url.html'), 404

    url_checks = urls_checks_repo.get_by_url_id(id)
    return render_template(
        'url.html',
        url_info=url_info,
        url_checks=url_checks,
        messages=get_flashed_messages(with_categories=True)
    )


@routes.post('/urls')
def urls_post():
    data = _get_form_data()
    url = data.get('url').strip()
    errors = validate_url(url)
    if errors:
        return _handle_validation_errors(errors, url)

    normalized_url = normalize_url(url)
    existing_urls = urls_repo.find_by_field('name', normalized_url)

    if existing_urls:
        url_info = existing_urls[0]
        url_id = url_info['id']
        flash(*FLASH_MESSAGES['url_exists'])
        return redirect(url_for('routes.urls_show', id=url_id), code=302)

    data['url'] = normalized_url
    new_url_record = urls_repo.save(data)
    url_id = new_url_record['id']
    flash(*FLASH_MESSAGES['url_added'])
    return redirect(url_for('routes.urls_show', id=url_id), code=302)


@routes.post('/urls/<int:id>/checks')
def url_checks_post(id):
    url_info = urls_repo.find(id)
    url = url_info['name']
    url_checker = URLChecker(url)
    new_check = url_checker.check() | {'url_id': id}

    if new_check['status_code'] != requests.codes.ok:
        flash(*FLASH_MESSAGES['url_check_error'])
    else:
        urls_checks_repo.save(new_check)
        flash(*FLASH_MESSAGES['url_checked'])

    return redirect(url_for('routes.urls_show', id=id), code=302)


def _get_form_data():
    return request.form.to_dict()


def _handle_validation_errors(errors, url):
    flash_errors(errors, 'url')
    return render_template(
        'index.html',
        url=url,
        messages=get_flashed_messages(with_categories=True)
    )


# TODO: remove after debugging

@routes.route('/checks')
def checks_index():
    checks = urls_checks_repo.get_content()
    return checks

@routes.route('/checks/<int:id>')
def checks_show(id):
    check = urls_checks_repo.find(id)
    return check

@routes.route('/conn')
def get_conn():
    return str(id(conn))
