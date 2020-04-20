import datetime
import jwt

from flask import current_app
from passlib.hash import sha512_crypt

from app.extensions import db
from app.models.__mixins import BaseFieldsMixin
from app.models.__tools import current_time, str_to_standard_datetime


class User(db.Model, BaseFieldsMixin):
    """User model """

    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(), nullable=True)
    last_login = db.Column(db.TIMESTAMP, nullable=True)
    last_logout = db.Column(db.TIMESTAMP, nullable=True)
    last_request = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, email, password, token=None, last_login=None, last_logout=None, last_request=None):
        self.email = email
        self.password = sha512_crypt.hash(password)
        self.token = token
        self.last_login = last_login
        self.last_logout = last_logout
        self.last_request = last_request

    def validate_password(self, password: str) -> bool:
        """ Check that given password is valid for given account

        :param password: password to be checked
        :return: True if password is valid equal, False otherwise
        """
        return sha512_crypt.verify(password, self.password)

    def update_password(self, old_password: str, password1: str, password2: str) -> bool:
        """ Update user password in DB

        :param old_password: old account password
        :param password1: new account password
        :param password2: new password confirmation
        :return: True if password are successfully updated, False otherwise
        """
        if not password1 == password2:
            return False

        if not self.validate_password(old_password):
            return False

        self.password = sha512_crypt.encrypt(password1)

        return True

    @staticmethod
    def are_passwords_equal(password1: str, password2: str) -> bool:
        """ Check given password(password1) and it's confirmation (password2) for equality

        :param password1: account password
        :param password2: password confirmation
        :return: True if passwords are equal, False otherwise
        """
        return password1 == password2

    @staticmethod
    def is_token_expired(token, secret_key: str) -> bool:
        """ Check user token for expiration

        :param token: user auth token
        :param secret_key: app secret key
        :return: True - token is expired, False - token is up to date
        """
        if not token:
            return True

        payload = jwt.decode(token, secret_key)
        expire, generated, user_id = (str_to_standard_datetime(payload['expire']),
                                      str_to_standard_datetime(payload['generated']),
                                      payload['user_id'])
        now = current_time()

        return now >= expire

    def create_auth_token(self, token_expiration_days: int, secret_key: str, algorithm: str) -> tuple:
        """ Create new access token for user

        :param token_expiration_days: how many days token should lives
        :param secret_key: app secret key
        :param algorithm: token crypto algorithm
        :return: created token, token generation datetime, token expiration datetime
        """
        generated = current_time()
        expire = generated + datetime.timedelta(days=token_expiration_days)
        payload = {
            'expire': str(expire),
            'generated': str(generated),
            'user_id': str(self.id_record)
        }
        token = jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)
        token = token.decode('utf-8')

        return token, generated, expire

    @staticmethod
    def decode_auth_token(auth_token):
        """ Decode the auth token
        :param auth_token: given token
        :return: token payload
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
