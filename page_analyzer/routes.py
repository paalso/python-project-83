from flask import Blueprint, render_template
from page_analyzer.db import get_db
from page_analyzer.repository import Repository

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
    return ('Trying to post!')


# TODO: remove after debugging
@routes.route('/conn')
def get_conn():
    conn = get_db()
    return str(id(conn))
