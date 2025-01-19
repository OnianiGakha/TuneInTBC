from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


app = Flask(__name__, static_folder="app/static")
app.config['SECRET_KEY'] = '90jrtyd90j87e9y7e4539w8y'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)

import routes
app.register_blueprint(routes.bp)

import models
