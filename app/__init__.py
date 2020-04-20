import config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.api import api_blueprint


app = Flask(__name__)
db = SQLAlchemy()

app.config.from_object(config)

db.init_app(app)
Migrate(app, db)

app.register_blueprint(api_blueprint)
