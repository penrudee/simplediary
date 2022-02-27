import os
from re import A 

from flask import Flask, request, current_app 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager
from config import Config 

db = SQLAlchemy()
migrate = Migrate() 


def create_app(config_class=Config):
    app_pos = Flask(__name__)
    app_pos.config.from_object(config_class)

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
   
    
    return app_pos


from app import models