
from app import app, db, mail
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from app.forms import UserInfoForm, LoginForm, PhonebookForm
from app.models import User

@app.route('/') 
def index():
    return render_template('index.html', title='Home' )


@app.route('/phonebook')
@login_required
def phonebookl():
    title = 'Phonebook'
    phonebooksp = phonebookl.query.all()
    return render_template('phonebook.html',title=title, phonebookso=phonebooksp)


@app.route('/register_phone_number', methods=['GET', 'POST'])
@login_required
def Register_Phone_Number():
    title = 'Register Phonebook'
    register_phone_form = PhonebookForm()
    if register_phone_form.validate_on_submit():
        first_name = register_phone_form.first_name.data
        last_name = register_phone_form.last_name.data
        phone_number = register_phone_form.phone_number.data
        address = register_phone_form.address.data

        new_phonebook = phonebookl(first_name, last_name, phone_number, address)
        
        db.session.add(new_phonebook)
        db.session.commit()

        flash(f'Thank you' , 'success')
        # Redirecting to the home page
        return redirect(url_for('phonebook'))

    return render_template('register_phone_number.html', title=title, form=register_phone_form)

@app.route('/register', methods= ["GET", "POST"])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).all()
        if existing_user:
            # Flash a warning message
            flash(f'The username {username} is already registered. Please try again.', 'danger')
            # Redirect back to the register page
            return redirect(url_for('register'))
       #create a new user instance
        new_user = User(username, email, password)
        #add the user
        db.session.add(new_user)
        db.session.commit()
        #redirect to the home page
        flash(f'thanx {username}', 'success')
        # Create Welcome Email to new user
        welcome_message = Message('Welcome!', [email])
        welcome_message.body = f' Thank you for signing up {username}.'
        # Send Welcome Email
        # mail.send(welcome_message)
        return redirect(url_for('index'))
    return render_template('register.html', form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #grab data from form
        username = form.username.data
        password = form.password.data
        
        #query our user table for a user w/username
        user = User.query.filter_by(username=username).first()
        
        #check if the user is none or if password is incorrect
        if user is None or not user.check_password(password):
         flash('incorrect password', 'danger')
         return redirect(url_for('login'))
        
        login_user(user)
        flash('Success!')
        return redirect(url_for('index'))
        
    return render_template('login.html', login_form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    

@app.route('/my-account')
@login_required
def my_account():
    return render_template('my_account.html')

