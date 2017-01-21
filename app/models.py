from app import db
import uuid
import enum


def generate_uuid():
   return str(uuid.uuid4())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=False)
    social_id = db.Column(db.String(64), nullable=False, unique=True, server_default="err")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class BookRecord(db.Model):
    uuid = db.Column(db.String, name="uuid", primary_key=True, default=generate_uuid)
    create_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(200), index=True, unique=False)
    book_type = db.Column(db.String(200), index=True, unique=False)
    author = db.Column(db.String(200), index=True, unique=False)
    description = db.Column(db.String(1024), index=True, unique=False)
    language = db.Column(db.String(100), index=True, unique=False)
    service_type = db.Column(db.String(100), index=True)
    target_place = db.Column(db.String(1024), index=True, unique=False)
    price = db.Column(db.Integer)
    is_exchanged = db.Column(db.Boolean, default=False, nullable=False)


class UserWantList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=False)


class ExchangeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_start = db.Column(db.Integer, default=0)
    to_start = db.Column(db.Integer, default=0)


