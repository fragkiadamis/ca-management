from flask import flash, redirect, render_template, url_for, request, session

from . import auth
from .forms import validate_form, login_required
from .. import db
from ..models import Member


@auth.route('/register', methods=['GET', 'POST'])
@validate_form(form_type='register')
def register():
    if request.method == 'POST':
        if len(request.errors):
            return {'errors': request.errors}

        data = request.json
        member = Member(first_name=data['first_name'], last_name=data['last_name'], username=data['username'],
                        email=data['email'], telephone=data['telephone'], semester=data['semester'],
                        uni_reg_number=data['uni_reg_number'],
                        address=f"{data['city']}, {data['address']}")
        member.hash(data['password'])
        # add member to the database
        db.session.add(member)
        db.session.commit()

        # redirect to the login page
        # flash('Το αίτημά σου καταχωρήθηκε, θα ενημερωθείς σύντομα με email.')
        return {'redirect': url_for('public.homepage')}

    # load registration template
    return render_template('register.html', title='Register')


@auth.route('/login', methods=['POST'])
def login():
    # data = request.json
    email = request.form['email']
    password = request.form['password']

    if (not email) or (not password):
        flash('Please fill in all the form fields')
        return redirect(url_for('public.homepage'))

    member = Member.query.filter_by(email=email).first()
    if member is not None and member.verify_hash(password):
        session['id'] = member.id
        session['username'] = member.username
        return redirect(url_for('public.about'))

    flash('Invalid email or password')
    return redirect(url_for('public.homepage'))


@auth.route('/logout')
@login_required
def logout():
    print("INSIDE")
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('public.homepage'))
