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

    def update_data(self, form):
        if form.password.data:
            self.password = form.password.data
        self.first_name = form.first_name.data
        self.last_name = form.last_name.data
        self.username = form.username.data
        self.email = form.email.data
        self.telephone = form.telephone.data
        self.city = form.city.data
        self.address = form.address.data
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def toggle_status(self, form):
        self.is_active = form.status.data
        db.session.commit()

    def verify(self):
        # Get last verified member's ca reg number and increase it to one and assign to new verified member
        last_member = Member.query.filter(Member.is_verified == 1).order_by(Member.id.desc()).first()
        incremental = int(''.join(x for x in last_member.ca_reg_number if x.isdigit())) + 1
        self.ca_reg_number = f'ca{incremental}'
        self.is_verified = self.is_active = 1
        db.session.commit()

    @staticmethod
    def filter_members(display):
        if display == 'pending':
            return {'Pending': Member.query.filter(Member.is_verified == 0)}
        elif display == 'active':
            return {'Active': Member.query.filter(Member.is_active == 1, Member.is_verified == 1)}
        elif display == 'inactive':
            return {'Inactive': Member.query.filter(Member.is_active == 0, Member.is_verified == 1)}
        elif display == 'admin':
            return {'Admin': Member.query.filter(Member.role == 'admin', Member.is_verified == 1)}
        elif display == 'ca_admin':
            return {'CA Admin': Member.query.filter(Member.role == 'ca_admin', Member.is_verified == 1)}
        elif display == 'basic':
            return {'Basic': Member.query.filter(Member.role == 'basic', Member.is_verified == 1)}
        elif display == 'role':
            all_members = Member.query.filter(Member.is_verified == 1)
            admins = [d for d in all_members if d.role == 'admin']
            ca_admins = [d for d in all_members if d.role == 'ca_admin']
            basics = [d for d in all_members if d.role == 'basic']
            return {'Admins': admins, 'CA Admins': ca_admins, 'Basic': basics}
        elif display == 'status':
            all_members = Member.query.filter(Member.is_verified == 1)
            active = [d for d in all_members if d.is_active]
            inactive = [d for d in all_members if not d.is_active]
            return {'Active': active, 'Inactive': inactive}
        else:
            return {'Current': Member.query.filter(Member.is_verified == 1, Member.is_active == 1)}


@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))
