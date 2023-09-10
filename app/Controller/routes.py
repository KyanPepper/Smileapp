from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post
from app.Controller.forms import PostForm

bp_routes = Blueprint("routes", __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER  #'..\\View\\templates'


@bp_routes.route("/", methods=["GET"])
@bp_routes.route("/index", methods=["GET"])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template("index.html", title="Smile Portal", posts=posts.all())


@bp_routes.route("/postsmile", methods=["GET", "POST"])
def create():
    cform = PostForm()
    if cform.validate_on_submit():
        newPost = Post(
            title=cform.title.data, body=cform.body.data, happiness_level=cform.happiness_level.data
        )
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