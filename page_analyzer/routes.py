from flask import (
    Blueprint,
    render_template
)

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/index')
def index():
    return render_template('index.html')


@routes.route('/urls')
def urls():
    return 'url list'
