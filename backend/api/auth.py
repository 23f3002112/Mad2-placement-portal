from flask import Blueprint, request, jsonify
from models import db, User, Student, Company
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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

    access_token = create_access_token(identity={"id": user.id, "role": user.role, "email": user.email})
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
    
    return jsonify({"msg": "Company registered successfully. Pending admin approval."}), 201
