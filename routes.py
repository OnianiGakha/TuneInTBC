from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from flask import Flask
from datetime import datetime
from models import User, Post, Reply, db
from dailyquestions import daily_questions as questions
from ext import app


admins = {"gakha1","gakha"}




bp = Blueprint('routes', __name__)


posts = []
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


UPLOAD_FOLDER2 = os.path.join('app', 'static', 'sounds')  
if not os.path.exists(UPLOAD_FOLDER2):  
    os.makedirs(UPLOAD_FOLDER2)

app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2



UPLOAD_FOLDER = os.path.join('app/static', 'imgs') 
if not os.path.exists(UPLOAD_FOLDER): 
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALBUMS_PATH = os.path.join("app", "static", "albums")
if not os.path.exists(ALBUMS_PATH):
    os.makedirs(ALBUMS_PATH)



app.config['ALBUMS_PATH'] = ALBUMS_PATH

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




image_files = [f for f in os.listdir(app.config['ALBUMS_PATH'])]


currentday = datetime.now().timetuple().tm_yday

questionoftheday = questions[currentday%len(questions)]

album = "none"#image_files[currentday % len(image_files)][0:-4]





@bp.route('/')
def home():
    
    
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']





    return render_template('home.html', username=username, admin = username in admins, albumoftheday=album)







    return redirect(url_for('routes.home'))


@bp.route('/profile', methods=['GET','POST'])
def profile():
    
    if request.method == 'GET':
        profileuser = request.args.get("profileuser")
    else:
        profileuser = request.form.get("profileuser")



    profile = User.query.filter(User.username == profileuser).first()
    print(profileuser)
    if profile:

        if 'username' not in session:
            username = "guest"
        else:
            username = session['username']

        if request.method == 'POST':
            
            print("postttt")



            if request.form.get("textColour") and request.form.get("textColour") != "#000000":

                profile.textcolor = str(request.form.get("textColour"))

            profile_audio = request.files.get("profileAudio")
            profile_image = request.files.get("profileImage")
            profile_banner = request.files.get("profileBanner")
            profile_background = request.files.get("profileBackground")
            profile_status = request.form.get("profileStatus")

            image_filename = None
            audio_filename = None
            banner_filename = None
            background_filename = None

            if request.form.get("postColour") and request.form.get("postColour") != "#000000":
                
                profile.postcolor = str(request.form.get("postColour"))



            print(profile_image.filename)
            

            if profile_image and allowed_file(profile_image.filename):
                image_filename = secure_filename(profile_image.filename)
                profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                profile.pfp = image_filename

            if profile_audio:
                audio_filename = secure_filename(profile_audio.filename)
                profile_audio.save(os.path.join(app.config['UPLOAD_FOLDER2'], audio_filename))
                profile.song = audio_filename

            if profile_banner:
                banner_filename = secure_filename(profile_banner.filename)
                profile_banner.save(os.path.join(app.config['UPLOAD_FOLDER2'], banner_filename))
                profile.banner = banner_filename

            if profile_background:
                background_filename = secure_filename(profile_background.filename)
                profile_background.save(os.path.join(app.config['UPLOAD_FOLDER2'], background_filename))
                profile.background = background_filename

            if profile_status:
                profile.aboutme = profile_status
            db.session.commit()

            return redirect(url_for('routes.profile', profileuser=profileuser))



        posts = Post.query.filter(Post.postername==profileuser).order_by(Post.post_date.desc()).all()

    
        return render_template('profile.html', username=username, admin = username in admins, profile=profile, posts=posts)
    else:
        return redirect(url_for('routes.home'))


    


@bp.route('/rockBoard')
def rockBoard():
    
    
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']

    
    posts = Post.query.filter(Post.board == "rockBoard").order_by(Post.post_date.desc()).all()

    return render_template('rockBoard.html', username=username, posts=posts, admin=username in admins)


@bp.route('/gearBoard')
def gearBoard():
    
    
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']

    
    posts = Post.query.filter(Post.board == "gearBoard").order_by(Post.post_date.desc()).all()

    return render_template('gearBoard.html', username=username, posts=posts, admin=username in admins)

@bp.route('/personalBoard')
def personalBoard():
    
    
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']

    
    posts = Post.query.filter(Post.board == "personalBoard").order_by(Post.post_date.desc()).all()

    return render_template('personalBoard.html', username=username, posts=posts, admin=username in admins)

@bp.route('/questionBoard')
def questionBoard():
    
    
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']

    
    posts = Post.query.filter(Post.board == "questionBoard").order_by(Post.post_date.desc()).all()

    return render_template('questionBoard.html', username=username, posts=posts, admin=username in admins, question=questionoftheday)


@bp.route('/generalBoard')
def generalBoard():
    
    
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']

    
    posts = Post.query.filter(Post.board == "generalBoard").order_by(Post.post_date.desc()).all()

    return render_template('generalBoard.html', username=username, posts=posts, admin=username in admins)

@bp.route('/reviewBoard')
def reviewBoard():
    
    
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']

    
    posts = Post.query.filter(Post.board == "reviewBoard").order_by(Post.post_date.desc()).all()

    return render_template('reviewBoard.html', username=username, posts=posts, admin=username in admins)

@bp.route('/thread', methods=['GET','POST'])
def thread():
    
    
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']

    
    
    thread=Post.query.filter(Post.id==request.args.get("postid")).first()

    print(request.args.get("postid"))

    replies = Reply.query.filter(Reply.thread == thread.id).order_by(Reply.reply_date.desc()).all()


    if thread:
        return render_template('thread.html', username=username, post=thread, replies=replies, admin = username in admins)
    else:
        render_template('home.html', username=username, admin = username in admins, albumoftheday=album)

    

@bp.route('/login', methods=['GET', 'POST'])
def login_view():
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username).first()
        if user and check_password_hash(user.password, password):
            
            session['username'] = username
            return redirect(url_for('routes.home'))
        else:
            return "error invalid credentials"
        
    return render_template('login.html', username=username, admin = username in admins)


@bp.route('/register', methods=['GET', 'POST'])
def register_view():
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if not User.query.filter(User.username == username).all() and 3<len(username)<20 and len(password)>5:

            new_user = User(username=username,email=email,password=generate_password_hash(password))
            new_user.save()


            session['username'] = username 
            return redirect(url_for('routes.home'))
        elif 3<len(username)<20 and len(password)>5:
            return "username is taken"
        elif len(password)>5:
            return "username should be larger than 3 letters and less than 20"
        else:
            return "password must be over 5 characters"
        
    return render_template('register.html', username=username, admin = username in admins)


@bp.route('/board', methods=['GET', 'POST'])
def board():
    if request.method == 'POST':
        title = request.form['title']
        post_text = request.form['postText']
        post_image = request.files.get('postImage')
        post_audio = request.files.get('postAudio')


        post_board = request.form.get('postBoard')

        timestamp = datetime.now()
        if 'username' not in session:
            username = "guest"
        else:
            username = session['username']
        user = username

        image_filename = None
        audio_filename = None

        

        if post_image and allowed_file(post_image.filename):
            image_filename = secure_filename(post_image.filename)
            post_image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        if post_audio:
            audio_filename = secure_filename(post_audio.filename)
            post_audio.save(os.path.join(app.config['UPLOAD_FOLDER2'], audio_filename))

        


        post = Post(postername=user,text=post_text,title=title,post_date=timestamp,board=post_board,image_path=image_filename,audio_path=audio_filename)
        post.save()


        return redirect(url_for('routes.' + post_board))

    posts = Post.query.filter(Post.board==post_board).order_by(Post.post_date.desc()).all()



    if 'username' not in session:
        return redirect(url_for('home.html', username="guest", albumoftheday=album))
    

    return render_template(post_board + '.html')



@bp.route('/logout')
def logout():

    session['username'] = 'guest'

    return render_template('home.html', username="guest", albumoftheday=album)


@bp.route('/deletethread', methods=["GET"])
def deletethread():
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']
    id = request.args.get("postid")
    print(id)

    post = Post.query.filter(Post.id == id).first()
    if post and post.postername == username:
        post.delete()

    return render_template('home.html', username=username, albumoftheday=album, admin=username in admins)



@bp.route('/deletereply', methods=["GET"])
def deletereply():
    print(request.url)
    id = request.args.get("replyid")
    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']
    print(id)
    reply = Reply.query.filter(Reply.id == id).first()

    if reply and (username == reply.postername or username in admins):
        reply.delete()

    

    return render_template('home.html', username=username, albumoftheday=album, admin=username in admins)


@bp.route('/search', methods=['GET'])
def search_posts():
    query = request.args.get('query', '') 
    board = request.args.get('postBoard', '')

    if 'username' not in session:
        username = "guest"
    else:
        username = session['username']
    post_query = Post.query

    if query:
        post_query = post_query.filter(
            (Post.title.ilike(f'%{query}%')) | (Post.text.ilike(f'%{query}%'))
        )

    if board and board != "all" and board != "profile":
        post_query = post_query.filter(Post.board.ilike(board))
        
    
    
    filtered_posts = post_query.order_by(Post.post_date.desc()).all()


    if board == "all":
        if query != "":

            return render_template('home.html', posts=filtered_posts, username=username, admin=username in admins, albumoftheday=album)

        else:
            return render_template('home.html', username=username, albumoftheday=album)

    elif board=="profile":
        post_query = post_query.filter(Post.postername == request.args.get("profileuser"))
        filtered_posts = post_query.order_by(Post.post_date.desc()).all()
        return render_template('home.html', posts=filtered_posts, username=username, admin=username in admins, albumoftheday=album)
    else:
        return render_template(board + '.html', posts=filtered_posts, username=username, admin=username in admins)





@bp.route('/reply', methods=['GET', 'POST'])
def reply():
    if request.method == 'POST':
        reply_text = request.form['postText']
        reply_image = request.files.get('postImage')
        reply_audio = request.files.get('postAudio')

        thread = request.form.get('thread')

        if 'username' not in session:
            username = "guest"
        else:
            username = session['username']

        post_board = request.form.get('postBoard')

        timestamp = datetime.now()

        user = username

        image_filename = None
        audio_filename = None

        

        if reply_image and allowed_file(reply_image.filename):
            image_filename = secure_filename(reply_image.filename)
            reply_image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        if reply_audio:
            audio_filename = secure_filename(reply_audio.filename)
            reply_audio.save(os.path.join(app.config['UPLOAD_FOLDER2'], audio_filename))

        


        reply = Reply(postername=user,text=reply_text,reply_date=timestamp,thread=thread,image_path=image_filename,audio_path=audio_filename)
        reply.save()
        replies = Reply.query.filter(Reply.thread == thread).order_by(Reply.reply_date.desc()).all()

        return redirect(url_for('routes.thread', postid=thread))






    

    if 'username' not in session:
        return redirect(url_for('routes.home', username="guest"))
    
    

    return render_template('thread.html',postid=request.form.get("thread"))

