from flask import Flask
from page_analyzer.routes import routes
from page_analyzer.db import close_db  # Импортируем close_db

app = Flask(__name__)
app.register_blueprint(routes)

app.teardown_appcontext(close_db)
