from flask_restplus import fields as restplus_fields
from marshmallow import Schema, fields as marshmallow_fields
from app.api import api


class UserValidator:
    """
    Series of tools to validate and process user info by application API
    """

    # Description of expected fields for Swagger documentation
    fields = api.model('User', {
        'email': restplus_fields.String(description='User email', required=True),
        'password': restplus_fields.String(description='User password', required=True),
    })

    class RequestValidator(Schema):
        """ Validates request data for described fields
        """
        email = marshmallow_fields.Email(required=True)
        password = marshmallow_fields.String(required=True)

    class ModelSerializer(Schema):
        """ Serializes model data.

        Example of usage:
            users = User.get_all()
            users = UserSchema(many=True).dump(users)
            return jsonify(users)
        """
        class Meta:
            """ Describes exposed model fields
            """
            fields = ("id", "email", "created", "updated", "last_login",
                      "last_logout", "last_request")
