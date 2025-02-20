from flask import Flask
from page_analyzer.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)
