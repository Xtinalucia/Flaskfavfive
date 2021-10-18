from app import app, db
from app.models import User, Post, Phonebook

if __name__ == '__main__':
    app.run()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Phonebook': Phonebook
    }