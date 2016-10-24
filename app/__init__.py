from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['BASE_DIR'] = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getcwd() + '/data/tweets.db'

db = SQLAlchemy(app)
db.engine.raw_connection().text_factory = str

import views
