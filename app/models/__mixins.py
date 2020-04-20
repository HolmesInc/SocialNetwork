from app.extensions import db


class BaseFieldsMixin:
    """ Add common model attributes to child model:

        id: int
        created: timestamp
        updated: timestamp

    """
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    updated = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now(), onupdate=db.func.now())