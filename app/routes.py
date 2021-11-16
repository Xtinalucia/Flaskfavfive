
from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from app.forms import UserInfoForm, LoginForm, PhonebookForm
from app.models import User, Phonebook
from flask import Blueprint, render_template




@app.route('/') 
def index():
    title = 'The Numbers'
    nums = Phonebook.query.all()
    return render_template('index.html', title=title, nums=nums ) 


# @app.route('/phonebook', methods=['GET'])#SHOW/DISPLAY all phonebook entries everything For ME
# @login_required
# def coffee_cup():
#     title = 'Phonebook'
#     phonebook = Phonebook.query.all()
#     return render_template('phonebook.html',title=title, phonebook=phonebook)


@app.route('/pnRegistery', methods=['POST']) # Not sure I need this?
@login_required
def Register_Phone_Number():
    title = 'Register Phonebook'
    register_phone_form = PhonebookForm()
    if register_phone_form.validate_on_submit():
        first_name = register_phone_form.first_name.data
        last_name = register_phone_form.last_name.data
        phone_number = register_phone_form.phone_number.data
        address = register_phone_form.address.data
        Phone_Book = Phonebook(first_name, last_name, phone_number, address)
        
        db.session.add(Phone_Book)
        db.session.commit()

        flash(f'Thank you' , 'success')
        # Redirecting to the home page
        return redirect(url_for('phonebook'))

    return render_template('pnRegistery.html', title=title, form=register_phone_form)

@app.route('/register', methods= ["GET", "POST"]) #Register to be able to login maybe 2 registeries are not necessary?
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
# How to delete ------------
@app.route('/my_account/delete/<phonebook_id>')
def deletePhoneEntry(phonebook_id):
    PhoneEntry = Phonebook.query.get(phonebook_id)#find the entry by id
    if not PhoneEntry is None:#if found
        db.session.delete(PhoneEntry)#delete entire entry
        db.session.commit()#commit
        
    return redirect('/')#refresh the page/#go bk to home page
    


@app.route('/my_account', methods=['GET', 'POST'])#Display current users info/enter number/edit/delete make similar to register_phone_number'
@login_required
def my_account():
    title = 'Account Details'
    phone_registry = PhonebookForm()#set  form to a variable
    if phone_registry.validate_on_submit():
        first_name = phone_registry.first_name.data
        last_name = phone_registry.last_name.data
        phone_number = phone_registry.phone_number.data
        address = phone_registry.address.data

        new_phonebook = Phonebook(first_name, last_name, phone_number, address)
        
        db.session.add(new_phonebook)
        db.session.commit()

        flash(f'Thank you' , 'success')
        # Redirecting to reigister 
        return redirect(url_for('index'))

    return render_template('pnRegistery.html', title=title, phone_registry=phone_registry)#gives access to info on html page







##########    LOGIN &&& LOGOUT   ################
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
        return redirect(url_for('my_account'))#takes u to the account page to view/edit
        
    return render_template('login.html', login_form=form) #takes you to ur form

@app.route('/logout')#LOGOUT WORKS WHEN URL IS INPUT
def logout():
    logout_user()
    return redirect(url_for('index'))
    


    

  

