from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.kamar import bp as kamar_bp
    app.register_blueprint(kamar_bp, url_prefix='/kamar')

    from app.routes.penghuni import bp as penghuni_bp
    app.register_blueprint(penghuni_bp, url_prefix='/penghuni')

    from app.routes.pembayaran import bp as pembayaran_bp
    app.register_blueprint(pembayaran_bp, url_prefix='/pembayaran')

    from app.routes.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    return app

from app import models
