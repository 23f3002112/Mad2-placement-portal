from flask import Flask
from models import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from api.auth import auth_bp
from api.admin import admin_bp
from api.company import company_bp
from api.student import student_bp
from celery_app import celery
from cache import cache

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppa.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key-ppa' # Change this in production
    
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(company_bp, url_prefix='/api/company')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    
    from api.notification import notification_bp
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    cache.init_app(app)
    
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
