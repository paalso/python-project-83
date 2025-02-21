from flask import (
    Blueprint,
    flash,
    get_flashed_messages,
    render_template,
    request
)
from page_analyzer.db import get_db
from page_analyzer.repository import Repository
from page_analyzer.validator import validate_url


def flash_errors(errors, key):
    for error in errors.get(key, []):
        flash(error, 'error')


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
    return render_template('/url.html')


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
            messages=messages
        )
    return 'All right!!!'


# TODO: remove after debugging
@routes.route('/conn')
def get_conn():
    conn = get_db()
    return str(id(conn))
