



from app.auth.routes import login
from app.main import main_bp
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models import Post
from app.forms import PostForm
from app import db 

import datetime 
import markdown
@main_bp.route("/")
@main_bp.route("/index")

def index():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(
    page=page,per_page= 2
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
        nw_post.body = markdown.markdown(form.body.data)
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
    return redirect(url_for('main_bp.allpost'))

@main_bp.route('/edit/<int:id>')
def edit(id):
    form = PostForm()
    
    po = Post.query.get(id)
    form.head.data = po.head 
    form.body.data = markdown.markdown(po.body)
    form.tag.data = po.tag
    form.img_url.data = po.img_url
    return render_template('edit.html',form=form,post=po)

@main_bp.route('/edit_post/<int:id>',methods=['POST'])
def edit_post(id):
    form = PostForm()
    po = Post.query.get(id)
    if request.method == 'POST':
        
        po.head = form.head.data 
        po.body = markdown.markdown(form.body.data) 
        po.tag = form.tag.data 
        po.img_url = form.img_url.data 
        
        db.session.add(po)
        db.session.commit()
    return redirect(url_for('main_bp.seepost',id=id))


@main_bp.route('/seepost/<int:id>')
def seepost(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("seepost.html",title="My Diary",post=post)

@main_bp.route('/tagpost/<string:tag>')
def tagpost(tag):
    page = request.args.get('page',1,type=int)
    posts = Post.query.filter_by(tag=tag).paginate(
    page=page,per_page= 2
  )
    return render_template('index.html',title="Tag",posts=posts.items,pge=posts)