from flask_restplus import Api
from flask import Blueprint

api = Api(version='0.0.0', title='Application API')
api_blueprint = Blueprint('api_blueprint', __name__, url_prefix="/api")
api.init_app(api_blueprint)
