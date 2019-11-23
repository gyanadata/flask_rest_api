from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    @staticmethod
    def username_password_match(_username, _password):
        user = User.query.filter_by(username=_username).filter_by(password=_password).first()
        if user is None:
            return False
        else:
            return True

    @staticmethod
    def create_user(_username, _password):
        new_user = User(username=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_all_user():
        return User.query.all()

    def __repr__(self):
        return str({"username": self.username, "password": self.password})
