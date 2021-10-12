from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hi Hi'

@app.route('/testlala')
def test():
    return 'test'

if __name__ == '__main__':
    app.run()
