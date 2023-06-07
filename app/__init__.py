"""
Initializes the app and all it's instances
"""
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

# initalizing the Flask app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # creating a database engine
migrate = Migrate(app, db) # creating a Migration engine
login = LoginManager(app)
mail = Mail(app)
login.login_view = "login"


# import all other modules
# Placed at the end to avoid Circular imports
from app import routes, models

@login.user_loader
def user_loader(id):
    return models.User.query.get(int(id))



    

