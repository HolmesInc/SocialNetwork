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
        'id': restplus_fields.String(description='User ID'),
        'created': restplus_fields.DateTime(description='User creation time'),
        'updated': restplus_fields.DateTime(description='Record last update'),
    })

    class RequestValidator(Schema):
        """ Validates request data for described fields
        """
        id = marshmallow_fields.String()
        email = marshmallow_fields.Email(required=True)
        created = marshmallow_fields.DateTime()
        updated = marshmallow_fields.DateTime()

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
            fields = ("id", "email", "created", "updated")
