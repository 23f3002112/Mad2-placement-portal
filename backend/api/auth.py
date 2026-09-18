from flask import Blueprint, request, jsonify
from models import db, User, Student, Company, Notification
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import json
from cache import cache
from mail import send_email
import string
import random

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad email or password"}), 401
        
    if not user.active:
        return jsonify({"msg": "Account is deactivated"}), 403
        
    if user.role == 'company':
        company = Company.query.filter_by(user_id=user.id).first()
        if company and not company.is_approved:
            return jsonify({"msg": "Company account is pending admin approval"}), 403

    access_token = create_access_token(identity=json.dumps({"id": user.id, "role": user.role, "email": user.email}))
    return jsonify(access_token=access_token, role=user.role)

@auth_bp.route('/register/student', methods=['POST'])
def register_student():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400
        
    hashed_pw = generate_password_hash(password)
    user = User(email=email, password=hashed_pw, role='student', active=True)
    db.session.add(user)
    db.session.commit()
    
    student = Student(user_id=user.id, name=name)
    db.session.add(student)
    db.session.commit()
    cache.clear()
    
    # Send Welcome Email and Notification
    subject = "Welcome to JobFinder!"
    body = f"Hello {name}, welcome to JobFinder! Your account has been created successfully."
    send_email(user.email, subject, body)
    
    notif = Notification(user_id=user.id, title=subject, message=body)
    db.session.add(notif)
    db.session.commit()
    
    return jsonify({"msg": "Student registered successfully"}), 201

@auth_bp.route('/register/company', methods=['POST'])
def register_company():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    company_name = data.get('company_name')
    
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400
        
    hashed_pw = generate_password_hash(password)
    user = User(email=email, password=hashed_pw, role='company', active=True)
    db.session.add(user)
    db.session.commit()
    
    company = Company(user_id=user.id, name=company_name, is_approved=False)
    db.session.add(company)
    db.session.commit()
    cache.clear()
    
    # Send Welcome Email and Notification
    subject = "Company Registration Pending"
    body = f"Hello {company_name}, thank you for registering on JobFinder! Your account is currently pending admin approval."
    send_email(user.email, subject, body)
    
    notif = Notification(user_id=user.id, title=subject, message=body)
    db.session.add(notif)
    
    # Notify admins
    admins = User.query.filter_by(role='admin').all()
    for admin in admins:
        admin_notif = Notification(
            user_id=admin.id,
            title="New Company Pending Approval",
            message=f"Company '{company_name}' has just registered and is waiting for your approval."
        )
        db.session.add(admin_notif)
        
    db.session.commit()
    
    return jsonify({"msg": "Company registered successfully. Pending admin approval."}), 201

@auth_bp.route('/google', methods=['POST'])
def google_login():
    data = request.get_json()
    token = data.get('credential') # This is the access_token from vue3-google-login
    
    try:
        import urllib.request
        import json as json_lib
        
        req = urllib.request.Request(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {token}'}
        )
        with urllib.request.urlopen(req) as response:
            user_info = json_lib.loads(response.read().decode())
            
        email = user_info['email']
        name = user_info.get('name', 'Google User')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create a new student user
            dummy_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            hashed_pw = generate_password_hash(dummy_password)
            user = User(email=email, password=hashed_pw, role='student', active=True)
            db.session.add(user)
            db.session.commit()
            
            student = Student(user_id=user.id, name=name)
            db.session.add(student)
            db.session.commit()
            cache.clear()
            
            # Send Welcome Email and Notification
            subject = "Welcome to JobFinder!"
            body = f"Hello {name}, welcome to JobFinder! Your account has been created successfully using Google Login."
            send_email(user.email, subject, body)
            
            notif = Notification(user_id=user.id, title=subject, message=body)
            db.session.add(notif)
            db.session.commit()
            
        if not user.active:
            return jsonify({"msg": "Account is deactivated"}), 403
            
        access_token = create_access_token(identity=json.dumps({"id": user.id, "role": user.role, "email": user.email}))
        return jsonify(access_token=access_token, role=user.role)
        
    except Exception as e:
        return jsonify({"msg": f"Google login failed: {str(e)}"}), 400
