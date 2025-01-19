from ext import app,db
from models import User,Post,Reply

with app.app_context():

    db.drop_all()
    db.create_all()
