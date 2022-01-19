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
    department = db.Column(db.Integer, db.ForeignKey('departments.id'))
    teams = db.relationship('Team', secondary='member_teams', back_populates="members")
    password_hash = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(60), unique=True, nullable=False)
    uni_reg_number = db.Column(db.String(60), unique=True, nullable=False)
    ca_reg_number = db.Column(db.String(60), unique=True)
    city = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
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
    telephone = db.Column(db.String(60), nullable=True)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    members = db.relationship('Member', secondary='member_teams', back_populates="teams")
    activities = db.relationship('Activity', secondary='team_activities', back_populates="teams")
    announcements = db.relationship('Announcement', secondary='team_announcements', back_populates="teams")
    files = db.relationship('File', secondary='team_files', back_populates="teams")

    @property
    def member_count(self):
        return len(self.members)

    @property
    def activity_count(self):
        return len(self.activities)

    @property
    def announcement_count(self):
        return len(self.announcements)

    @property
    def file_count(self):
        return len(self.files)


class MemberTeams(db.Model):
    __tablename__ = 'member_teams'

    id = db.Column(db.Integer(), primary_key=True)
    member_id = db.Column(db.Integer(), db.ForeignKey('members.id', ondelete='CASCADE'))
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))


class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
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
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    members = db.relationship("Member")

    @property
    def member_count(self):
        return len(self.members)


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(60), nullable=False)
    body = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    update_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    teams = db.relationship('Team', secondary='team_announcements', back_populates="announcements")
    added_by = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)


class TeamAnnouncements(db.Model):
    __tablename__ = 'team_announcements'

    id = db.Column(db.Integer(), primary_key=True)
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))
    announcement_id = db.Column(db.Integer(), db.ForeignKey('announcements.id', ondelete='CASCADE'))


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    update_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    start_time = db.Column(db.Time(), nullable=False)
    end_time = db.Column(db.Time(), nullable=False)
    teams = db.relationship('Team', secondary='team_activities', back_populates="activities")
    added_by = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)


class TeamActivities(db.Model):
    __tablename__ = 'team_activities'

    id = db.Column(db.Integer(), primary_key=True)
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))
    activity_id = db.Column(db.Integer(), db.ForeignKey('activities.id', ondelete='CASCADE'))


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    teams = db.relationship('Team', secondary='team_files', back_populates="files")
    added_by = db.Column(db.Integer(), db.ForeignKey('members.id'), nullable=False)


class TeamFiles(db.Model):
    __tablename__ = 'team_files'

    id = db.Column(db.Integer(), primary_key=True)
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))
    file_id = db.Column(db.Integer(), db.ForeignKey('files.id', ondelete='CASCADE'))


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Float(precision=2), nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    update_date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    description = db.Column(db.Text(255), nullable=True)
    type = db.Column(db.String(60), nullable=False)
    added_by = db.Column(db.Integer(), db.ForeignKey('members.id'))
    updated_by = db.Column(db.Integer(), db.ForeignKey('members.id'))
    team = db.Column(db.Integer(), db.ForeignKey('teams.id'))
    member = db.Column(db.Integer(), db.ForeignKey('members.id'))
    # commission = db.relationship('Transaction', backref='assoc_transactions')
    commissions = db.relationship('Commission', secondary='transaction_commissions', cascade="all, delete-orphan", single_parent=True)


class Commission(db.Model):
    __tablename__ = 'commissions'

    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Float(precision=2), nullable=False)
    description = db.Column(db.Text(255), nullable=True)


class TransactionCommissions(db.Model):
    __tablename__ = 'transaction_commissions'

    id = db.Column(db.Integer(), primary_key=True)
    transaction_id = db.Column(db.Integer(), db.ForeignKey('transactions.id'))
    commission_id = db.Column(db.Integer(), db.ForeignKey('commissions.id'))
