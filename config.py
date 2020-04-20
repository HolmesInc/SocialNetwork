import os
import pathlib

ROOT_DIR = pathlib.Path(
    os.path.abspath(os.path.dirname(__file__))
)
SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/{db_name}'.format(
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"] + ":" + os.environ["POSTGRES_PORT"],
    db_name=os.environ["POSTGRES_DB"])
