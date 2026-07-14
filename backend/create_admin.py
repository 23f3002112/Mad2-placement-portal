import os
from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    
    admin_email = 'admin@institute.com'
    admin_exists = User.query.filter_by(email=admin_email).first()
    
    if not admin_exists:
        print(f"Creating Admin user...")
        hashed_pw = generate_password_hash('111')
        admin_user = User(email=admin_email, password=hashed_pw, role='admin', active=True)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user {admin_email} created successfully.")
    else:
        print(f"Admin user {admin_email} already exists.")
