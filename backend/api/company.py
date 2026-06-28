from flask import Blueprint, request, jsonify
from models import db, User, Student, Company, JobPosition, Application
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

company_bp = Blueprint('company', __name__)

def get_company_or_403():
    current_user = get_jwt_identity()
    if current_user.get('role') != 'company':
        return None, jsonify({"msg": "Unauthorized role"}), 403
        
    company = Company.query.filter_by(user_id=current_user['id']).first()
    if not company:
        return None, jsonify({"msg": "Company profile not found"}), 404
        
    if not company.is_approved:
        return None, jsonify({"msg": "Company is pending admin approval"}), 403
        
    return company, None, None

@company_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    active_jobs = JobPosition.query.filter_by(company_id=company.id, status='Approved').count()
    
    total_jobs = JobPosition.query.filter_by(company_id=company.id).count()
    
    job_ids = [j.id for j in JobPosition.query.filter_by(company_id=company.id).all()]
    total_applications = Application.query.filter(Application.job_id.in_(job_ids)).count() if job_ids else 0
    shortlisted = Application.query.filter(Application.job_id.in_(job_ids), Application.status == 'Shortlisted').count() if job_ids else 0
    
    return jsonify({
        "active_jobs": active_jobs,
        "total_jobs": total_jobs,
        "applications": total_applications,
        "shortlisted": shortlisted
    }), 200

@company_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    if request.method == 'GET':
        return jsonify({
            "name": company.name,
            "industry": company.industry,
            "location": company.location,
            "description": company.description
        }), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        company.industry = data.get('industry', company.industry)
        company.location = data.get('location', company.location)
        company.description = data.get('description', company.description)
        db.session.commit()
        return jsonify({"msg": "Profile updated successfully"}), 200

@company_bp.route('/jobs', methods=['GET', 'POST'])
@jwt_required()
def manage_jobs():
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    if request.method == 'GET':
        jobs = JobPosition.query.filter_by(company_id=company.id).all()
        result = []
        for j in jobs:
            result.append({
                "id": j.id,
                "title": j.title,
                "description": j.description,
                "salary": j.salary,
                "skills_required": j.skills_required,
                "status": j.status,
                "created_at": j.created_at
            })
        return jsonify(result), 200
        
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        salary = data.get('salary')
        skills_required = data.get('skills_required')
        
        job = JobPosition(
            company_id=company.id,
            title=title,
            description=description,
            salary=salary,
            skills_required=skills_required,
            status='Pending'
        )
        db.session.add(job)
        db.session.commit()
        return jsonify({"msg": "Job created and pending admin approval"}), 201

@company_bp.route('/jobs/<int:job_id>/status', methods=['PUT'])
@jwt_required()
def update_job_status(job_id):
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first_or_404()
    
    data = request.get_json()
    new_status = data.get('status')
    
    if job.status in ['Pending', 'Rejected']:
        return jsonify({"msg": "Cannot change status of unapproved job"}), 400
        
    if new_status in ['Approved', 'Closed']:
        job.status = new_status
        db.session.commit()
        return jsonify({"msg": "Job status updated successfully"}), 200
    
    return jsonify({"msg": "Invalid status"}), 400

@company_bp.route('/jobs/<int:job_id>/applications', methods=['GET'])
@jwt_required()
def get_job_applications(job_id):
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first_or_404()
    applications = Application.query.filter_by(job_id=job.id).all()
    
    result = []
    for app in applications:
        student = Student.query.get(app.student_id)
        result.append({
            "id": app.id,
            "student_name": student.name,
            "education": student.education,
            "skills": student.skills,
            "status": app.status,
            "feedback": app.feedback,
            "interview_date": app.interview_date.isoformat() if app.interview_date else None,
            "date_applied": app.date_applied
        })
    return jsonify(result), 200

@company_bp.route('/applications/<int:app_id>/status', methods=['PUT'])
@jwt_required()
def update_application_status(app_id):
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    application = Application.query.get_or_404(app_id)
    job = JobPosition.query.get(application.job_id)
    
    if job.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403
        
    data = request.get_json()
    new_status = data.get('status')
    feedback = data.get('feedback')
    interview_date = data.get('interview_date')
    
    if new_status:
        application.status = new_status
    if feedback is not None:
        application.feedback = feedback
    if interview_date:
        application.interview_date = datetime.fromisoformat(interview_date.replace('Z', '+00:00'))
        
    db.session.commit()
    return jsonify({"msg": "Application updated successfully"}), 200
