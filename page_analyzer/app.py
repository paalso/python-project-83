from flask import Flask
from page_analyzer.routes import routes
from dotenv import load_dotenv
import os
import logging


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    app.register_blueprint(routes)
    return app


app = create_app()
