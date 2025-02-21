from flask import Flask
from page_analyzer.routes import routes
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(routes)
