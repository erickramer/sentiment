from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/eric/Projects/sentiment/data/tweets.db'
app.config['BASE_DIR'] = os.getcwd()

db = SQLAlchemy(app)
db.engine.raw_connection().text_factory = str

import views
