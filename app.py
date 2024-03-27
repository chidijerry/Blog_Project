# app.py
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import Config
from flask_login import LoginManager

from werkzeug.exceptions import HTTPException
import logging

db = SQLAlchemy()
login_manager = LoginManager()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    with app.app_context():
        from .models import BlogPost, Admin
        from .routes import main as main_blueprint
        login_manager.login_view = 'login'
        app.register_blueprint(main_blueprint)

        @app.route('/')
        @app.route('/blog')
        def view_blog():
            # put application's code here
            return render_template('view_blog_post.html', values = BlogPost.query.all())
    return app


@login_manager.user_loader
def load_user(user_id):
    from .models import Admin
    return Admin.query.get(int(user_id))




if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
