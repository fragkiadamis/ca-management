from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Member(db.Model, UserMixin):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)
    telephone = db.Column(db.String(60), unique=True, nullable=False)
    semester = db.Column(db.String(60), nullable=False)
    uni_reg_number = db.Column(db.String(60), unique=True, nullable=False)
    ca_reg_number = db.Column(db.String(60), unique=True)
    address = db.Column(db.String(60), nullable=False)
    # department_id = db.Column(db.Integer, nullable=False)
    # team_id = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<Member: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))
