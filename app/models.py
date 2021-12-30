from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Member(UserMixin, db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    role = db.Column(db.String(60), nullable=False, default='basic')
    password_hash = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(60), unique=True, nullable=False)
    semester = db.Column(db.String(60), nullable=False)
    uni_reg_number = db.Column(db.String(60), unique=True, nullable=False)
    ca_reg_number = db.Column(db.String(60), unique=True)
    city = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

# Teams
class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False)
    # teamMembers = db.Column()
    description = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    telephone = db.Column(db.String(60), unique=True, nullable=False)


# # Treasury
# class Treasury(db.Model):
#     id = db.Column(db.Float, primary_key=True, nullable=False, unique=True)
#     totalSum = db.Column(db.Float, nullable=False)
#     caBalance = db.Column(db.Float, nullable=False)
#
#
# class TeamTreasury(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     balance = db.Column(db.Float, nullable=False)
#     # team = db.Column()
#
#
# class Transaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     amount = db.Column(db.Float, nullable=False)
#     # addedBy = db.Column()
#     # team = db.Column()
#     transactionDate = db.Column(db.Date, nullable=False)
#     description = db.Column(db.String(60), nullable=False)
#
#
# # class Subscription:
# #     # member = db.Column()
# #     semester = db.Column(db.String(60), nullable=False)
# #
# #
# # class RegistrationFee:
# #     # member = db.Column()
# #     name = db.Column(db.String(60)) # de xreiazetai
#
#
# # Files
# class File(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     name = db.Column(db.String(60), nullable=False)
#     path = db.Column(db.String(60), nullable=False)
#     type = db.Column(db.String(60), nullable=False)
#
#
# # Institutions
# class Institution(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     name = db.Column(db.String(60), nullable=False)
#
#
# class School(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     name = db.Column(db.String(60), nullable=False)
#     # institution = db.Column()
#
#
# class Department(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     name = db.Column(db.String(60), nullable=False)
#     # school = db.Column()
#
#
# # Announcements
# class Announcement(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     title = db.Column(db.String(60), nullable=False)
#     description = db.Column(db.String(60), nullable=False)
#     createDate = db.Column(db.Date, nullable=True)
#     # addedBy = db.Column()
#
#
# # Activities
# class Activity(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     title = db.Column(db.String(60), nullable=False)
#     description = db.Column(db.String(60), nullable=False)
#     createDate = db.Column(db.Date, nullable=True)
#     activityDate = db.Column(db.Date, nullable=True)

