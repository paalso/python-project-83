from flask import (
    Blueprint,
    flash,
    get_flashed_messages,
    jsonify,
    render_template,
    request
)
from page_analyzer.db import get_db
from page_analyzer.repository import Repository
from page_analyzer.validator import validate_url
from urllib.parse import urlparse


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
repo = Repository(conn)


@routes.route('/')
@routes.route('/index')
def index():
    return render_template('index.html')


@routes.route('/urls')
def urls():
    urls = repo.get_content()
    return render_template('/urls.html', urls=urls)


@routes.route('/urls/<int:id>')
def url_info(id):
    url = repo.find(id)
    return url


@routes.post('/urls')
def urls_post():
    data = request.form.to_dict()
    url = data.get('url')
    errors = validate_url(url)
    if errors:
        flash_errors(errors, 'url')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            url=url,
            messages=messages
        )

    normalized_url = normalize_url(url)
    new_url_record = repo.create(normalized_url)
    flash('Страница успешно добавлена', 'success')
    if new_url_record:
        return render_template(
            '/url.html',
            url_record=new_url_record,
            messages = get_flashed_messages(with_categories=True)
        )
    return 'Already exists'


@routes.post('/urls/<int:id>/checks')
def check_url(id):
    return f'Checking url with {id}...'


# TODO: remove after debugging
@routes.route('/conn')
def get_conn():
    return str(id(conn))


@routes.route('/urls/find/<path:url>')
def url_by_name(url):
    result = repo.find_by_field("name", url)
    if result:
        return jsonify(result), 200
    return jsonify({"error": "URL not found"}), 404
