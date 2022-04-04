import os
import logging


from re import A 

from flask import Flask, request, current_app 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager
from config import Config
from momentjs import momentjs 
from logging.handlers import SMTPHandler, RotatingFileHandler

db = SQLAlchemy()
migrate = Migrate() 


def create_app(config_class=Config):
    app_pos = Flask(__name__)
    app_pos.config.from_object(config_class)
    app_pos.jinja_env.globals['momentjs'] = momentjs
    db.init_app(app_pos)
    migrate.init_app(app_pos,db)
    login_manager = LoginManager()
    login_manager.login_view ='auth_bp.login'
    login_manager.init_app(app_pos)


    




    from .models import User 
    
    @login_manager.user_loader 
    def load_user(user_id):
        return User.query.get(int(user_id))




    from app.auth import auth_bp 
    from app.main import main_bp
    


    app_pos.register_blueprint(auth_bp)
    app_pos.register_blueprint(main_bp)
   
    if not app_pos.debug and not app_pos.testing:
        if app_pos.config['MAIL_SERVER']:
            auth = None
            if app_pos.config['MAIL_USERNAME'] or app_pos.config['MAIL_PASSWORD']:
                auth = (app_pos.config['MAIL_USERNAME'],
                    app_pos.config['MAIL_PASSWORD'])
            secure = None
            if app_pos.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app_pos.config['MAIL_SERVER'], app_pos.config['MAIL_PORT']),
                fromaddr='no-reply@' + app_pos.config['MAIL_SERVER'],
                toaddrs=app_pos.config['ADMINS'], subject='Pharmbookdiary Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app_pos.logger.addHandler(mail_handler)

        if app_pos.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app_pos.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/pharmbookdiary.log',
                                            maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app_pos.logger.addHandler(file_handler)

        app_pos.logger.setLevel(logging.INFO)
        app_pos.logger.info('PharmbookDiary startup')
     
    return app_pos


from app import models