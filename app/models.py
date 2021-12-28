from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(60), unique=True, nullable=False)
    semester = db.Column(db.String(60), nullable=False)
    uni_reg_number = db.Column(db.String(60), unique=True, nullable=False)
    ca_reg_number = db.Column(db.String(60), unique=True)
    address = db.Column(db.String(60), nullable=False)

    def hash(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Member: {}>'.format(self.username)
