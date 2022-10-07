



from app.auth.routes import login
from app.main import main_bp
from flask import redirect, render_template, request, url_for,flash
from flask_login import current_user, login_required
from app.models import Post,Comment
from app.forms import PostForm,CommentForm
from app import db 


import datetime 
import markdown
import emoji
import random

avatar_list=["https://i.imgur.com/XgiReFb.png",
"https://i.imgur.com/YhL3357.png",
"https://i.imgur.com/a6qPMz0.png",
"https://i.imgur.com/oSFvmDv.png",
"https://i.imgur.com/j0kLy71.png",
"https://i.imgur.com/uWvpTb7.png",
"https://i.imgur.com/mA1pFH2.png",
"https://i.imgur.com/7b0PAnK.png",
"https://i.imgur.com/nh0Bbli.png",
"https://i.imgur.com/8hxwIn8.png",
"https://i.imgur.com/SbDPxT9.png",
"https://i.imgur.com/JJ2KC6Q.png",
"https://i.imgur.com/boGvkPY.png",
"https://i.imgur.com/gyneFoF.png",
"https://i.imgur.com/QHYQDst.png"]


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
@main_bp.app_template_filter('emojify')
def emoji_filter(s):
    return emoji.emojize(s)

    
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
    seepostid = post.id
    seepost_img_url=post.img_url
    return render_template("seepost.html",title="My Diary",post=post,seepostid=seepostid,seepost_img_url=seepost_img_url)

@main_bp.route('/tagpost/<string:tag>')
def tagpost(tag):
    page = request.args.get('page',1,type=int)
    posts = Post.query.filter_by(tag=tag).paginate(
    page=page,per_page= 2
  )
    return render_template('index.html',title="Tag",posts=posts.items,pge=posts)

@main_bp.route('/comments/<int:id>',methods=['GET','POST'])
def comments(id):
    post = Post.query.filter_by(id=id).first()
    form = CommentForm()
    rand = random.choice(avatar_list)
    if form.validate_on_submit():
        _c = Comment()
        _c.body = form.body.data
        _c.email = form.email.data 
        _c.timestamp = datetime.datetime.now()
        _c.post_id = post.id
        _c.approve = False 
        _c.avatar = rand 
        db.session.add(_c)
        db.session.commit()
        flash("โปรดรอให้แอดมิน approve comment","success")
    else:
        comment=Comment.query.filter_by(post_id=post.id)
        return render_template("comments.html",
                                title="My Diary",
                                post=post,
                                form=form,
                                comment=comment,
                                
                                )
    comment=Comment.query.filter_by(post_id=post.id)
    return render_template("comments.html",
                                title="My Diary",
                                post=post,
                                form=form,
                                comment=comment,
                               
                                )
@main_bp.route("/allcomment")
def allcomment():
    allcomment = Comment.query.order_by(Comment.id.desc())
    return render_template("allcomment.html",
                            title="All Comment",
                            allcomment=allcomment)

@main_bp.route('/approve_comment/<int:id>',methods=['POST'])
def approve_comment(id):
    if request.method=="POST":
        c = Comment.query.filter_by(id=id).first()
        c.approve = True 
        db.session.add(c)
        db.session.commit()
        flash("Approve comment ","success")
        return redirect(url_for('main_bp.allcomment'))

@main_bp.route('/delete_comment/<int:id>',methods=['POST'])
def delete_comment(id):
    if request.method == "POST":
        c = Comment.query.filter_by(id=id).first()
        db.session.delete(c)
        db.session.commit()
        flash("ลบเรียบร้อย","danger")
    return redirect(url_for('main_bp.allcomment'))