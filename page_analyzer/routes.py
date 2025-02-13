from flask import Blueprint

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/index')
def index():
    return 'Hello from Flask!'
