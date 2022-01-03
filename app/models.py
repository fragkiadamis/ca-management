from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Member(db.Model, UserMixin):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    roles = db.relationship('Roles', secondary='member_roles')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    teams = db.relationship('Team', secondary='member_teams')
    password_hash = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(60), unique=True, nullable=False)
    uni_reg_number = db.Column(db.String(60), unique=True, nullable=False)
    ca_reg_number = db.Column(db.String(60), unique=True)
    city = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    registration_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    update_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())

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


class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class MemberRoles(db.Model):
    __tablename__ = 'member_roles'

    id = db.Column(db.Integer(), primary_key=True)
    member_id = db.Column(db.Integer(), db.ForeignKey('members.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True)
    telephone = db.Column(db.String(60), unique=True)
    members = db.relationship('Member', secondary='member_teams')

    @property
    def member_count(self):
        return len(self.members)


class MemberTeams(db.Model):
    __tablename__ = 'member_teams'

    id = db.Column(db.Integer(), primary_key=True)
    member_id = db.Column(db.Integer(), db.ForeignKey('members.id', ondelete='CASCADE'))
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False)
    path = db.Column(db.String(60), nullable=False, unique=True)
    type = db.Column(db.String(60), nullable=False)


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    createDate = db.Column(db.Date, nullable=True)
    # addedBy = db.Column()


# Activities
class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    createDate = db.Column(db.DateTime(timezone=True), server_default=func.now())
    activityDate = db.Column(db.DateTime(timezone=True), nullable=False)


class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60))
    departments = db.relationship("Department", cascade="all, delete-orphan")

    @property
    def member_count(self):
        count = 0
        for department in self.departments:
            verified_members = filter(lambda member: member.is_verified, department.members)
            count += len(list(verified_members))
        return count


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.String(60))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    members = db.relationship("Member")

    @property
    def member_count(self):
        return len(self.members)
