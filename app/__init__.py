import config
from flask import Flask
from flask_migrate import Migrate

from app.api.users import UsersResource
from app.extensions import db
from app.api import api_blueprint


app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)
Migrate(app, db)

app.register_blueprint(api_blueprint)
