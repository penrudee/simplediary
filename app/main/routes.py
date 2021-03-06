


from app.auth.routes import login
from app.main import main_bp
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models import Post
from app.forms import PostForm
from app import db 
import datetime 

@main_bp.route("/")
@main_bp.route("/index")
@login_required
def index():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(
    page=page,per_page= 3
  )
  
    return render_template('index.html',
                            title="Home",
                            posts=posts.items,
                            pge=posts)


@main_bp.route('/newpost')
@login_required
def newpost():
    form = PostForm()
    return render_template('post.html',
                            title="New Post",
                            form=form)

@main_bp.route('/post_post',methods=['POST'])
def post_post():
    form = PostForm()
    if request.method == "POST":
        nw_post=Post()
        nw_post.head = form.head.data 
        nw_post.body = form.body.data
        nw_post.img_url = form.img_url.data 
        nw_post.tag = form.tag.data 
        nw_post.user_id = current_user.id 
        nw_post.timestamp = datetime.datetime.now()
        db.session.add(nw_post)
        db.session.commit()
        return redirect(url_for('main_bp.index'))

@main_bp.route('/allpost')
@login_required
def allpost():
    posts = Post.query.all()
    return render_template('allpost.html',
                            title="Allpost",
                            posts=posts)
@main_bp.route('/del_post/<int:id>',methods=['POST'])
@login_required
def del_post(id):
    p = Post.query.get(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('allpost'))


@main_bp.route('/seepost/<int:id>')
def seepost(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("seepost.html",title="My Diary",post=post)