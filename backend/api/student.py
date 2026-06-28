from flask import Blueprint, request, jsonify
from models import db, User, Student, Company, JobPosition, Application
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

student_bp = Blueprint('student', __name__)

def get_student_or_403():
    current_user = json.loads(get_jwt_identity())
    if current_user.get('role') != 'student':
        return None, jsonify({"msg": "Unauthorized role"}), 403
        
    student = Student.query.filter_by(user_id=current_user['id']).first()
    if not student:
        return None, jsonify({"msg": "Student profile not found"}), 404
        
    return student, None, None

@student_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    applications = Application.query.filter_by(student_id=student.id).all()
    total_applications = len(applications)
    shortlisted = len([a for a in applications if a.status == 'Shortlisted'])
    selected = len([a for a in applications if a.status == 'Selected'])
    rejected = len([a for a in applications if a.status == 'Rejected'])
    
    return jsonify({
        "applications": total_applications,
        "shortlisted": shortlisted,
        "selected": selected,
        "rejected": rejected
    }), 200

@student_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    if request.method == 'GET':
        return jsonify({
            "name": student.name,
            "education": student.education,
            "skills": student.skills,
            "resume_url": student.resume_url,
            "experience": student.experience
        }), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        student.education = data.get('education', student.education)
        student.skills = data.get('skills', student.skills)
        student.resume_url = data.get('resume_url', student.resume_url)
        student.experience = data.get('experience', student.experience)
        db.session.commit()
        return jsonify({"msg": "Profile updated successfully"}), 200

@student_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    search = request.args.get('search', '').lower()
    
    query = JobPosition.query.filter_by(status='Approved')
    
    if search:
        query = query.join(Company).filter(
            db.or_(
                db.func.lower(JobPosition.title).contains(search),
                db.func.lower(JobPosition.skills_required).contains(search),
                db.func.lower(Company.name).contains(search)
            )
        )
        
    jobs = query.all()
    result = []
    
    applied_job_ids = [a.job_id for a in Application.query.filter_by(student_id=student.id).all()]
    
    for j in jobs:
        result.append({
            "id": j.id,
            "title": j.title,
            "description": j.description,
            "salary": j.salary,
            "skills_required": j.skills_required,
            "company_name": j.company.name if j.company else "Unknown",
            "has_applied": j.id in applied_job_ids,
            "created_at": j.created_at
        })
    return jsonify(result), 200

@student_bp.route('/applications', methods=['GET', 'POST'])
@jwt_required()
def manage_applications():
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    if request.method == 'GET':
        applications = Application.query.filter_by(student_id=student.id).all()
        result = []
        for app in applications:
            job = JobPosition.query.get(app.job_id)
            result.append({
                "id": app.id,
                "job_title": job.title,
                "company_name": job.company.name if job.company else "Unknown",
                "status": app.status,
                "feedback": app.feedback,
                "interview_date": app.interview_date.isoformat() if app.interview_date else None,
                "date_applied": app.date_applied
            })
        return jsonify(result), 200
        
    if request.method == 'POST':
        data = request.get_json()
        job_id = data.get('job_id')
        
        job = JobPosition.query.filter_by(id=job_id, status='Approved').first()
        if not job:
            return jsonify({"msg": "Job not found or not approved"}), 404
            
        existing_app = Application.query.filter_by(student_id=student.id, job_id=job.id).first()
        if existing_app:
            return jsonify({"msg": "You have already applied for this job"}), 400
            
        new_app = Application(
            student_id=student.id,
            job_id=job.id,
            status='Applied'
        )
        db.session.add(new_app)
        db.session.commit()
        return jsonify({"msg": "Application submitted successfully"}), 201
