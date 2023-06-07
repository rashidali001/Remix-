import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.getenv("SECRET_KEY") or "mysecretkey"
    # DATABASE CONFIGURATIONS
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or \
        "sqlite:///"+os.path.join(basedir, "remix.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # EMAIL CONFIGURATIONS
    MAIL_SERVER = os.getenv("EMAIL_SERVER")
    MAIL_PORT = os.getenv("EMAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    ADMINS = ["rashidestonian@gmail.com"]
