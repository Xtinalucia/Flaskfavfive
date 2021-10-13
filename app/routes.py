
from app import app
from flask import render_template
from app.forms import UserInfoForm, PostForm
from app.models import User, Post
from app import db

@app.route('/')
def index():
    name = 'Tatyana...'
    title = 'These are a few of my favourite things...'
    return render_template('index.html', name_of_user=name, title=title)

@app.route('/pg1')
def test():
    title = 'Giant Slayer'
    return render_template('pg1.html')
'<a class="2019 RWC Fights" href="https://www.youtube.com/watch?v=RGrb0LoT6eg">SCUFFLES & BLACKEYES</a>'

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
        print(username, email, password)
        new_user = User(username,email,password)
        db.session.add(new_user)
        db.session.commit()
              
    return render_template('register.html', form=register_form)

@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_post = Post(title, content, user_id=1)
        db.session.add(new_post)
        db.session.commit()
    return render_template('createpost.html', form=form)


