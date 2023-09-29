from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post,Tag,postTags
from app.Controller.forms import PostForm,SortForm

bp_routes = Blueprint("routes", __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER  #'..\\View\\templates'

@bp_routes.route("/", methods=["GET", "POST"])
@bp_routes.route("/index", methods=["GET", "POST"])
def index():
    sform = SortForm()
    posts = None 
    
    if sform.validate_on_submit():
        if sform.sort.data == 1:
            posts = Post.query.order_by(Post.timestamp.desc()).all()
        elif sform.sort.data == 2:
            posts = Post.query.order_by(Post.title.desc()).all()
        elif sform.sort.data == 3:
            posts = Post.query.order_by(Post.likes.desc()).all()
        else:
            posts = Post.query.order_by(Post.happiness_level.desc()).all()
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).all()
    ptotal = Post.query.count()
  
    return render_template("index.html", title="Smile Portal", posts=posts, ptotal=ptotal, form=sform)

@bp_routes.route("/postsmile", methods=["GET", "POST"])
def create():
    cform = PostForm()
    if cform.validate_on_submit():
        newPost = Post(
            title=cform.title.data, body=cform.body.data, happiness_level=cform.happiness_level.data
        )
        t1 = cform.tag.data
        for tag in t1:
            newPost.tags.append(tag)

        db.session.add(newPost)
        db.session.commit()
        flash('Succsesfuly Submitted Smile')
        return(redirect(url_for('routes.index')))
    return render_template("create.html", title="Post Form", form=cform)


@bp_routes.route("/like/<post_id>", methods=["POST","GET"])
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Post doesnt exist')
        return redirect(url_for('routes.index'))  
    else:
        post.likes+=1
        db.session.commit()
    return redirect(url_for('routes.index'))