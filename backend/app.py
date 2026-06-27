from flask import Flask
from models import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from api.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppa.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key-ppa' # Change this in production
    
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
