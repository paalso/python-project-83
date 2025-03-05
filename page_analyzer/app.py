import logging
import os

from dotenv import load_dotenv
from flask import Flask

from page_analyzer.routes import routes


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s")

    app.register_blueprint(routes)
    return app


app = create_app()
