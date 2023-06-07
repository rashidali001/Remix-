from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from time import time



class User(UserMixin,db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64))
    phone_no = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(100), unique=True, index=True)   
    hash_password = db.Column(db.String(200))  
    points = db.Column(db.Integer)  

    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def set_password(self, password):
        self.hash_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hash_password, password)
    
    # SETTING JWT TOKEN
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password':self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256')    

    # VERIFYING JWT TOKEN
    def verify_password_reset_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])["reset_password"]
        except:
            return
                
        return User.query.get(id)
    
    def __repr__(self):
        return f"<user: {self.username}>"       


class Employees(UserMixin, db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    id_no = db.Column(db.Integer, unique=True, index=True)
    fullname = db.Column(db.String(64))
    hash_password = db.Column(db.String(20))
    hash_pin = db.Column(db.String(20))

    def __init__(self, fullname, id_no):
        self.fullname = fullname
        self.id_no = id_no

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    def set_pin(self, pin):
        self.hash_pin = generate_password_hash(pin)

    def check_pin(self, pin):
        return check_password_hash(self.hash_pin, pin)

    def __repr__(self):
        return f"<Employee: {self.fullname}>"        


