from flask import (
    Blueprint,
    render_template
)
from  page_analyzer.tmp_dummy_data import data

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/index')
def index():
    return render_template('index.html')


@routes.route('/urls')
def urls():
    return render_template(
        '/urls.html',
        urls=data
    )


@routes.route('/urls/<int:id>')
def url_info(id):
    return render_template(
        '/url.html'
    )


@routes.post('/urls')
def urls_post():
    return 'Trying to post!'
