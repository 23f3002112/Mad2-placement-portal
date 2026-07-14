from flask import Blueprint, request, jsonify
from models import db, User, Student, Company, JobPosition, Application, Placement
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from cache import cache

company_bp = Blueprint('company', __name__)

import json

def get_company_or_403():
    current_user = json.loads(get_jwt_identity())
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
        search = request.args.get('search', '').lower()
        query = JobPosition.query.filter_by(company_id=company.id)
        
        if search:
            query = query.filter(
                db.or_(
                    db.func.lower(JobPosition.title).contains(search),
                    db.func.lower(JobPosition.skills_required).contains(search)
                )
            )
            
        jobs = query.all()
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
        cache.clear()
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
        cache.clear()
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
        user = User.query.get(student.user_id)
        result.append({
            "id": app.id,
            "student_name": student.name,
            "education": student.education,
            "skills": student.skills,
            "resume_url": student.resume_url,
            "experience": student.experience,
            "email": user.email if user else "",
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
        if new_status == 'Placed':
            existing_placement = Placement.query.filter_by(student_id=application.student_id, job_id=job.id).first()
            if not existing_placement:
                placement = Placement(
                    student_id=application.student_id,
                    company_id=company.id,
                    job_id=job.id,
                    position_offered=job.title,
                    salary_offered=job.salary
                )
                db.session.add(placement)
    if feedback is not None:
        application.feedback = feedback
    if interview_date:
        application.interview_date = datetime.fromisoformat(interview_date.replace('Z', '+00:00'))
        
    db.session.commit()
    return jsonify({"msg": "Application updated successfully"}), 200

from models import ExportJob
from tasks import export_csv_task
from flask import send_file
import os

@company_bp.route('/export', methods=['POST'])
@jwt_required()
def trigger_export():
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    current_user = json.loads(get_jwt_identity())
    export_job = ExportJob(user_id=current_user['id'], status='Pending')
    db.session.add(export_job)
    db.session.commit()
    
    export_csv_task(export_job.id, current_user['id'], 'company')
    
    return jsonify({"msg": "Export task started", "job_id": export_job.id}), 202

@company_bp.route('/exports', methods=['GET'])
@jwt_required()
def get_exports():
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    current_user = json.loads(get_jwt_identity())
    jobs = ExportJob.query.filter_by(user_id=current_user['id']).order_by(ExportJob.created_at.desc()).all()
    result = [{"id": j.id, "status": j.status, "created_at": j.created_at} for j in jobs]
    return jsonify(result), 200

@company_bp.route('/exports/<int:job_id>/download', methods=['GET'])
@jwt_required()
def download_export(job_id):
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    current_user = json.loads(get_jwt_identity())
    job = ExportJob.query.filter_by(id=job_id, user_id=current_user['id']).first_or_404()
    if job.status != 'Completed' or not job.file_path:
        return jsonify({"msg": "File not ready"}), 400
        
    return send_file(os.path.abspath(job.file_path), as_attachment=True)

from models import Message

@company_bp.route('/messages/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    job_ids = [j.id for j in JobPosition.query.filter_by(company_id=company.id).all()]
    applications = Application.query.filter(Application.job_id.in_(job_ids), Application.status.in_(['Shortlisted', 'Selected', 'Placed', 'Offer'])).all()
    
    result = []
    for app in applications:
        student = Student.query.get(app.student_id)
        job = JobPosition.query.get(app.job_id)
        last_msg = Message.query.filter_by(application_id=app.id).order_by(Message.timestamp.desc()).first()
        
        result.append({
            "application_id": app.id,
            "student_name": student.name,
            "student_id": student.user_id,
            "job_title": job.title,
            "last_message": last_msg.content if last_msg else None,
            "last_timestamp": last_msg.timestamp.isoformat() if last_msg else None,
            "status": app.status
        })
    
    result.sort(key=lambda x: x['last_timestamp'] or '', reverse=True)
    return jsonify(result), 200

@company_bp.route('/messages/<int:application_id>', methods=['GET', 'POST'])
@jwt_required()
def handle_messages(application_id):
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    app = Application.query.get_or_404(application_id)
    job = JobPosition.query.get(app.job_id)
    if job.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403
        
    if app.status not in ['Shortlisted', 'Selected', 'Placed', 'Offer', 'Interview']:
        return jsonify({"msg": "Cannot message candidate unless shortlisted"}), 403
        
    current_user = json.loads(get_jwt_identity())
    student = Student.query.get(app.student_id)
    
    if request.method == 'GET':
        messages = Message.query.filter_by(application_id=application_id).order_by(Message.timestamp.asc()).all()
        result = []
        for m in messages:
            result.append({
                "id": m.id,
                "sender_id": m.sender_id,
                "content": m.content,
                "timestamp": m.timestamp.isoformat()
            })
        return jsonify(result), 200
        
    if request.method == 'POST':
        data = request.get_json()
        content = data.get('content')
        if not content:
            return jsonify({"msg": "Content is required"}), 400
            
        new_msg = Message(
            sender_id=current_user['id'],
            receiver_id=student.user_id,
            application_id=application_id,
            content=content
        )
        db.session.add(new_msg)
        db.session.commit()
        
        return jsonify({
            "id": new_msg.id,
            "sender_id": new_msg.sender_id,
            "content": new_msg.content,
            "timestamp": new_msg.timestamp.isoformat()
        }), 201
