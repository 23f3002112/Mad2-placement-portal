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
    
    user = User.query.get(company.user_id)
    if user:
        from mail import send_email
        from models import Notification
        
        subject = "Your Company Profile is Approved!"
        body = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 0 auto; padding: 30px; border: 1px solid #eaeaea; border-radius: 12px; background-color: #ffffff;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #00008b; margin: 0; font-size: 28px;">Job<span style="color: #ff3e6c;">Finder</span></h1>
            </div>
            <h2 style="color: #28a745; text-align: center; margin-bottom: 20px;">Congratulations, {company.name}! 🎉</h2>
            <p style="font-size: 16px; color: #4a4a4a; line-height: 1.6;">Your company registration on JobFinder has been successfully approved by our administration team.</p>
            <p style="font-size: 16px; color: #4a4a4a; line-height: 1.6;">You can now log in to your company dashboard to start posting placement drives and discovering top student talent.</p>
            <div style="text-align: center; margin: 40px 0;">
                <a href="http://localhost:5173/login" style="background-color: #00008b; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 50px; font-weight: 600; font-size: 16px; display: inline-block;">Go to Dashboard</a>
            </div>
            <p style="font-size: 14px; color: #888888; border-top: 1px solid #f0f0f0; padding-top: 20px; text-align: center;">Welcome aboard,<br/><strong>The JobFinder Team</strong></p>
        </div>
        """
        send_email(user.email, subject, body, content="html")
        
        notif = Notification(user_id=user.id, title=subject, message="Your company profile has been officially approved. You can now post jobs.")
        db.session.add(notif)
        
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
    
    company = job.company
    if company:
        user = User.query.get(company.user_id)
        if user:
            to_email = company.contact_email if company.contact_email else user.email
            from mail import send_email
            subject = f"Your job post '{job.title}' has been approved!"
            body = f"Hello {company.name},\n\nGreat news! Your recent job posting for '{job.title}' has been approved by our administration team. It is now live and visible to all students on the platform.\n\nBest regards,\nPlacement Portal Admin"
            send_email(to_email, subject, body)
            
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

from models import Notification, Message, Placement

@admin_bp.route('/companies/<int:company_id>', methods=['DELETE'])
@jwt_required()
def delete_company_endpoint(company_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    company = Company.query.get_or_404(company_id)
    user = User.query.get(company.user_id)
    
    jobs = JobPosition.query.filter_by(company_id=company.id).all()
    for job in jobs:
        apps = Application.query.filter_by(job_id=job.id).all()
        for app in apps:
            Message.query.filter_by(application_id=app.id).delete()
            db.session.delete(app)
        Placement.query.filter_by(job_id=job.id).delete()
        db.session.delete(job)
        
    Placement.query.filter_by(company_id=company.id).delete()
    
    db.session.delete(company)
    if user:
        db.session.delete(user)
        
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Company and all associated data deleted successfully"}), 200

@admin_bp.route('/students/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student_endpoint(student_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    
    apps = Application.query.filter_by(student_id=student.id).all()
    for app in apps:
        Message.query.filter_by(application_id=app.id).delete()
        db.session.delete(app)
        
    Placement.query.filter_by(student_id=student.id).delete()
    
    db.session.delete(student)
    if user:
        db.session.delete(user)
        
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Student and all associated data deleted successfully"}), 200

@admin_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job_endpoint(job_id):
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    job = JobPosition.query.get_or_404(job_id)
    
    apps = Application.query.filter_by(job_id=job.id).all()
    for app in apps:
        Message.query.filter_by(application_id=app.id).delete()
        db.session.delete(app)
        
    Placement.query.filter_by(job_id=job.id).delete()
    
    db.session.delete(job)
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Job deleted successfully"}), 200

@admin_bp.route('/search', methods=['GET'])
@jwt_required()
def global_search():
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    query_str = request.args.get('q', '').lower()
    if not query_str:
        return jsonify({"companies": [], "students": [], "jobs": []}), 200
        
    # Search Companies
    companies_query = Company.query.filter(db.or_(
        db.func.lower(Company.name).contains(query_str),
        db.func.lower(Company.industry).contains(query_str)
    )).all()
    
    companies_result = []
    for c in companies_query:
        user = User.query.get(c.user_id)
        companies_result.append({
            "id": c.id, "name": c.name, "industry": c.industry,
            "location": c.location, "is_approved": c.is_approved,
            "is_active": user.active if user else False
        })
        
    # Search Students
    students_query = Student.query.filter(db.or_(
        db.func.lower(Student.name).contains(query_str),
        db.func.lower(Student.skills).contains(query_str)
    )).all()
    
    students_result = []
    for s in students_query:
        user = User.query.get(s.user_id)
        students_result.append({
            "id": s.id, "name": s.name, "education": s.education,
            "email": user.email if user else "",
            "is_active": user.active if user else False
        })
        
    # Search Jobs
    jobs_query = JobPosition.query.join(Company).filter(db.or_(
        db.func.lower(JobPosition.title).contains(query_str),
        db.func.lower(JobPosition.skills_required).contains(query_str),
        db.func.lower(Company.name).contains(query_str)
    )).all()
    
    jobs_result = []
    for j in jobs_query:
        jobs_result.append({
            "id": j.id, "title": j.title, 
            "company_name": j.company.name if j.company else "Unknown",
            "status": j.status, "created_at": j.created_at
        })
        
    return jsonify({
        "companies": companies_result,
        "students": students_result,
        "jobs": jobs_result
    }), 200

@admin_bp.route('/notifications/send', methods=['POST'])
@jwt_required()
def send_notification():
    if not admin_required():
        return jsonify({"msg": "Unauthorized"}), 403
        
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    message = data.get('message')
    
    if not user_id or not title or not message:
        return jsonify({"msg": "Missing fields: user_id, title, message"}), 400
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    notif = Notification(user_id=user.id, title=title, message=message)
    db.session.add(notif)
    db.session.commit()
    
    return jsonify({"msg": "Notification sent successfully"}), 200
