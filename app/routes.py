
from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import UserInfoForm, PostForm, LoginForm
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
def index():
    title = 'These are a few of my favourite things...'
    posts = Post.query.all()
    return render_template('index.html', title=title,  posts=posts)

@app.route('/pg1')
def test():
    title = 'Giant Slayer'
    return render_template('pg1.html')
'<a class="2019 RWC Fights" href="https://www.youtube.com/watch?v=RGrb0LoT6eg">SCUFFLES & BLACKEYES</a>'
# finish ^ this

@app.route('/RWC')
def Rugby():
    title = 'Highlight Reel'
    reel = ['tries not Touchdowns', 'no helmets','you pass to the side, never forward','you can kick','much easier on the eyes than that other sport']
    return render_template('RWC.html', title=title, reel =reel)

@app.route('/register', methods= ['GET', 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        print('Hello hi')
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
        new_user = User(username,email,password)
        #add the user
        db.session.add(new_user)
        db.session.commit()
        
        #redirect to the home page
        flash(f'thanx {username}', 'success')
        
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
        if not user is None or not user.check_password(password):
            flash('incorrect password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user)
        flash('Success!')
        return redirect(url_for('index'))
        
    return render_template('login.html', login_form=form, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
        


@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        print('hi')
        title = form.title.data
        content = form.content.data
        new_post = Post(title, content, current_user.id)
        db.session.add(new_post)
        db.session.commit()
    
    flash(f'The post {title} has been created.', 'primary')
    return redirect(url_for('index'))
        
    return render_template('createpost.html', form=form)

@app.route('/PhoneBook', methods=['GET', 'POST'])
def phonenumber():
    title = 'PhoneBook'
    PhoneBook_form = UserInfoForm()
    if PhoneBook_form.validate_on_submit():
        first_name = PhoneBook_form.first_name.data
        last_name = PhoneBook_form.last_name.data
        number = PhoneBook_form.number.data
        address = PhoneBook_form.address.data
        new_user = User(first_name,last_name,number, address)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Well that worked.')
        return redirect(url_for('index'))
              
    return render_template('PhoneBook.html', title=title, form=PhoneBook_form)
