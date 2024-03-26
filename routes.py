from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user

from .forms import LoginForm
from .models import Admin, BlogPost
from .app import db

from .services import create_admin, user_login_manager, upload_blog_posts, save_blog_post_edit, remove_blog_post
# Create a Blueprint named 'main'
main = Blueprint('main', __name__)


@main.route('/signup', methods=['GET', 'POST'])
def signup_admin():
    if request.method == 'POST':
        create_admin(request.form.get("full_name"), request.form.get("admin_email"), request.form.get("admin_password"))
    return render_template('create_admin_user.html')


@main.route('/login', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm()
    if current_user.is_authenticated:
        return render_template('create_blog_post.html')

    if request.method == 'POST' and form.validate_on_submit():
        if user_login_manager(form):
            return render_template('create_blog_post.html')
        else:
            flash('Invalid email or password', 'error')
            return render_template('login_admin_user.html', form=form)
    return render_template('login_admin_user.html', form=form)


@main.route('/create_blog', methods=['GET'])
def create_blog_post():
    if current_user.is_authenticated:
        return render_template('create_blog_post.html')
    return render_template('view_blog_post.html')


@main.route('/edit_blog_post', methods=['GET'])
def edit_blog_post():
    if current_user.is_authenticated:
        post = BlogPost.query.filter_by(admin_id=current_user.id).all()
        return render_template('edit_blog_post.html',values=post)
    return render_template('view_blog_post.html')


@main.route('/delete_blog_post', methods=['GET'])
def delete_blog_post():
    if current_user.is_authenticated:
        post = BlogPost.query.filter_by(admin_id=current_user.id).all()
        return render_template('delete_blog_post.html', values = post)
    return render_template('view_blog_post.html')



## uploads the blog
@main.route('/upload_blog', methods=['POST'])
def upload_blog_post():
    upload_blog_posts(request.form.get("blog_title"), request.form.get("blog_content"))## admin_id yet to be done
    return render_template('create_blog_post.html')


## save changes to the blog
@main.route('/save_changes', methods=['POST'])
def save_changes():
    save_blog_post_edit(request.form.get("blog_title"),request.form.get("blog_content"),request.form.get("blog_id"))
    post = BlogPost.query.filter_by(admin_id=current_user.id).all()
    return render_template('edit_blog_post.html', values=post)


@main.route('/remove_blog', methods=['POST'])
def remove_blog():
    post = BlogPost.query.filter_by(admin_id=current_user.id).all()
    remove_blog_post(request.form.get("blog_id"))
    return 'Blog post deleted', 200


@main.route('/logout', methods=['POST'])
def logout_admin():
    logout_user()
    return redirect(url_for('main.login_admin'))
