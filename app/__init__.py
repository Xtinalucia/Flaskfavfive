from flask import Flask
from config import Config
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate= Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message ='need to login first'
login_manager.login_message_category = 'danger'

from app import routes, models