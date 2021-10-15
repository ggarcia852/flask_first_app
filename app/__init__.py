from flask import Flask
from config import Config
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)  ####for signin
login_manager.login_view = 'login'
login_manager.login_message = 'You must login first to view this page'
login_manager.login_message_category = 'danger'

mail = Mail(app)

from app import routes, models
