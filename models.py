from ext import db, login_manager
from flask_login import UserMixin

class BaseModel():
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


class User(db.Model,BaseModel, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    pfp = db.Column(db.String(), nullable=True)
    aboutme = db.Column(db.String(), nullable=True)
    song = db.Column(db.String(),nullable=True)
    banner = db.Column(db.String(),nullable=True)
    background = db.Column(db.String(),nullable=True)
    textcolor = db.Column(db.String(),nullable=True)
    postcolor = db.Column(db.String(),nullable=True)



class Post(db.Model,BaseModel):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True) 
    postername = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    image_path = db.Column(db.String(), nullable=True)
    audio_path = db.Column(db.String(), nullable=True)
    post_date = db.Column(db.DateTime, nullable=False)
    board = db.Column(db.String(), nullable=False)

class Reply(db.Model,BaseModel):
    __tablename__ = "replies"
    id = db.Column(db.Integer, primary_key=True)
    postername = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
    image_path = db.Column(db.String(), nullable=True)
    audio_path = db.Column(db.String(), nullable=True)
    reply_date = db.Column(db.DateTime, nullable=False)
    thread = db.Column(db.String(), nullable=False)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
