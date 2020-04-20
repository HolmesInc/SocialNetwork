from http import HTTPStatus

from flask_restplus import Resource
from flask import jsonify, request, abort, make_response
from app.api import api
from app.validators import UserValidator
from app.models import User


user_namespace = api.namespace('users/', description='User management API')
api.add_namespace(user_namespace)


@user_namespace.route('/users/')
class UsersResource(Resource):
    """ Describes HTTP methods of users endpoint
    """

    def get(self):
        """ HTTP GET handler of users endpoint
        """
        users = User.get_all()
        users = UserValidator.ModelSerializer(many=True).dump(users)
        return make_response(jsonify(users), HTTPStatus.OK)

    @api.expect([UserValidator.fields])
    def post(self):
        """ HTTP POST handler of users endpoint
        """
        data = request.json
        errors = UserValidator.RequestValidator(many=True).validate(data)
        if errors:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, str(errors))
        users = User.bulk_create(data)
        users = UserValidator.ModelSerializer(many=True).dump(users)
        return make_response(jsonify(users), HTTPStatus.CREATED)
