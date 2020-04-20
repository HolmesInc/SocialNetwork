from http import HTTPStatus

from flask_restplus import Resource
from flask import jsonify, request, abort, make_response
from app.api import api
from app.validators import UserValidator
from app.models import User
from app.extensions import db


user_namespace = api.namespace('users/', description='User management API')
api.add_namespace(user_namespace)


@user_namespace.route('/user/')
class UsersResource(Resource):
    """ Describes HTTP methods of users endpoint
    """

    @api.expect(UserValidator.fields)
    def post(self):
        """ User Sign Up
        """
        data = request.json
        errors = UserValidator.RequestValidator().validate(data)
        if errors:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, str(errors))

        User.create(data)

        return make_response(jsonify({"message": "User has created"}))

    @api.expect(UserValidator.fields)
    def put(self):
        """ User login
        """
        data = request.json
        errors = UserValidator.RequestValidator().validate(data)
        if errors:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, str(errors))

        user = db.session.query(User).filter_by(email=data['email']).first()
        if user and user.validate_password(data['password']):
            return make_response(jsonify({"message": "User logged in", "token": user.token}))

        return make_response(jsonify({"message": "Invalid user data"}))
