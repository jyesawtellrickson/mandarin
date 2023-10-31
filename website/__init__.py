from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .static import utils
import os

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('WEBSITE_SECRET_KEY', None)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECURE_REFERRER_POLICY'] = "no-referrer-when-downgrade"

    db.init_app(app)

    # just adding this breaks the app
    @app.context_processor
    def text_processor():
        def h2p(text, together):
            return utils.hanyu_to_pinyin(text, together)
        def h2s(text):
            return utils.hanyu_to_structured(text)
        def s2h(s, l):
            return utils.structured_to_html(s, l)
        def ap(s):
            return utils.get_pinyin(s)
        def gv(t):
            return utils.generate_vocab(t)
        def u2e(u):
            return utils.url_to_embed(u)
        return dict(h2p=h2p, h2s=h2s, s2h=s2h, ap=ap, gv=gv, u2e=u2e)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
