from flask import Blueprint, request, jsonify
from models import db, User, Student, Company, JobPosition, Application
from flask_jwt_extended import jwt_required, get_jwt_identity
from cache import cache

admin_bp = Blueprint('admin', __name__)

import json

def admin_required():
    current_user = json.loads(get_jwt_identity())
    if current_user.get('role') != 'admin':
        return False
    return True

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
    
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = JobPosition.query.count()
    total_applications = Application.query.count()
    
    return jsonify({
        "students": total_students,
        "companies": total_companies,
        "jobs": total_jobs,
        "applications": total_applications
    }), 200

@admin_bp.route('/companies', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_companies():
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    search = request.args.get('search', '').lower()
    query = Company.query
    if search:
        query = query.filter(db.or_(
            db.func.lower(Company.name).contains(search),
            db.func.lower(Company.industry).contains(search)
        ))
    
    companies = query.all()
    result = []
    for c in companies:
        user = User.query.get(c.user_id)
        result.append({
            "id": c.id,
            "name": c.name,
            "industry": c.industry,
            "location": c.location,
            "is_approved": c.is_approved,
            "is_active": user.active if user else False
        })
    return jsonify(result), 200

@admin_bp.route('/companies/<int:company_id>/approve', methods=['POST'])
@jwt_required()
def approve_company(company_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    company = Company.query.get_or_404(company_id)
    company.is_approved = True
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Company approved successfully"}), 200

@admin_bp.route('/companies/<int:company_id>/reject', methods=['POST'])
@jwt_required()
def reject_company(company_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    company = Company.query.get_or_404(company_id)
    user = User.query.get(company.user_id)
    if user:
        db.session.delete(user)
    db.session.delete(company)
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Company rejected and removed"}), 200

@admin_bp.route('/companies/<int:company_id>/blacklist', methods=['POST'])
@jwt_required()
def blacklist_company(company_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    company = Company.query.get_or_404(company_id)
    user = User.query.get(company.user_id)
    if user:
        user.active = not user.active
        db.session.commit()
        cache.clear()
        status = "deactivated" if not user.active else "activated"
        return jsonify({"msg": f"Company {status} successfully"}), 200
    return jsonify({"msg": "User not found"}), 404

@admin_bp.route('/students', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_students():
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    search = request.args.get('search', '').lower()
    query = Student.query
    if search:
        query = query.filter(db.func.lower(Student.name).contains(search))
        
    students = query.all()
    result = []
    for s in students:
        user = User.query.get(s.user_id)
        result.append({
            "id": s.id,
            "name": s.name,
            "education": s.education,
            "email": user.email if user else "",
            "is_active": user.active if user else False
        })
    return jsonify(result), 200

@admin_bp.route('/students/<int:student_id>/blacklist', methods=['POST'])
@jwt_required()
def blacklist_student(student_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    if user:
        user.active = not user.active
        db.session.commit()
        cache.clear()
        status = "deactivated" if not user.active else "activated"
        return jsonify({"msg": f"Student {status} successfully"}), 200
    return jsonify({"msg": "User not found"}), 404

@admin_bp.route('/jobs', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def get_jobs():
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    jobs = JobPosition.query.all()
    result = []
    for j in jobs:
        result.append({
            "id": j.id,
            "title": j.title,
            "company_name": j.company.name if j.company else "Unknown",
            "status": j.status,
            "created_at": j.created_at
        })
    return jsonify(result), 200

@admin_bp.route('/jobs/<int:job_id>/approve', methods=['POST'])
@jwt_required()
def approve_job(job_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    job = JobPosition.query.get_or_404(job_id)
    job.status = 'Approved'
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Job approved successfully"}), 200

@admin_bp.route('/jobs/<int:job_id>/reject', methods=['POST'])
@jwt_required()
def reject_job(job_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    job = JobPosition.query.get_or_404(job_id)
    job.status = 'Rejected'
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Job rejected successfully"}), 200

@admin_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_all_applications():
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    applications = Application.query.all()
    result = []
    for app in applications:
        student = Student.query.get(app.student_id)
        job = JobPosition.query.get(app.job_id)
        result.append({
            "id": app.id,
            "student_name": student.name,
            "job_title": job.title,
            "company_name": job.company.name if job.company else "Unknown",
            "status": app.status,
            "date_applied": app.date_applied,
            "student_id": student.id
        })
    return jsonify(result), 200

@admin_bp.route('/students/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_details(student_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    
    applications = Application.query.filter_by(student_id=student.id).all()
    apps_data = []
    for app in applications:
        job = JobPosition.query.get(app.job_id)
        apps_data.append({
            "id": app.id,
            "job_title": job.title,
            "company_name": job.company.name if job.company else "Unknown",
            "status": app.status,
            "date_applied": app.date_applied
        })
        
    return jsonify({
        "id": student.id,
        "name": student.name,
        "education": student.education,
        "skills": student.skills,
        "resume_url": student.resume_url,
        "experience": student.experience,
        "email": user.email if user else "",
        "applications": apps_data
    }), 200
