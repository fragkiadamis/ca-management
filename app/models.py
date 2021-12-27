from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Member(UserMixin, db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    firstName = db.Column(db.String(60), nullable=False)
    lastName = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<Member: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))
