from flask_login import login_user, current_user

from blogProject.models import Admin, BlogPost
from . import db


# functions for routes

# create admin  into admin table
def create_admin(admin_name, admin_email, admin_password):
    store_admin = Admin(user_name=admin_name, email=admin_email)
    store_admin.set_password(admin_password)
    db.session.add(store_admin)
    db.session.commit()
    return True


def user_login_manager(form):
    user = Admin.query.filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
        return False
    login_user(user)
    return True


# uploads the created blog
def upload_blog_posts(blog_title, blog_content):
    user_id = current_user.id
    new_blog_post = BlogPost(title=blog_title, content=blog_content, admin_id=user_id)
    db.session.add(new_blog_post)
    db.session.commit()
    return True


# save blog edit
def save_blog_post_edit(blog_title, blog_content, blog_id):
    post_to_update = BlogPost.query.filter_by(id=blog_id).first()
    post_to_update.title = blog_title
    post_to_update.content = blog_content
    db.session.commit()
    return True  # Indicate success


# delete blog post
def remove_blog_post(blog_post_id):
    blog_post_to_delete = BlogPost.query.filter_by(id=blog_post_id).first()
    db.session.delete(blog_post_to_delete)
    db.session.commit()
    return True
