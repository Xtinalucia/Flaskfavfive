from app import app
from flask import render_template

@app.route('/')
def home():
    name = 'Tatyana...'
    title = 'These are a few of my favourite things...'
    return render_template('index.html', name_of_user=name, title=title)

@app.route('/pg1')
def test():
    return '<a class="2019 RWC Fights" href="https://www.youtube.com/watch?v=RGrb0LoT6eg">SCUFFLES & BLACKEYES</a>'

@app.route('/RWC')
def Rug():
    title = 'Highlight Reel'
    reel = ['tries not Touchdowns', 'no helmets','you pass to the side, never forward','you can kick','much easier on the eyes than that other sport']
    return render_template('RWC.html', title=title, reel =reel)

