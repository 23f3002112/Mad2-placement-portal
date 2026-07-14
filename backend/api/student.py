from flask import Blueprint, request, jsonify, send_file
from models import db, User, Student, Company, JobPosition, Application, ExportJob, Placement
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import os
from cache import cache
from tasks import export_csv_task
from werkzeug.utils import secure_filename
from tasks import export_csv_task

def make_user_cache_key(*args, **kwargs):
    return request.path + request.query_string.decode('utf-8') + str(get_jwt_identity())

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
            "experience": student.experience,
            "photo_url": student.photo_url,
            "location": student.location,
            "linkedin": student.linkedin,
            "github": student.github
        }), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        student.name = data.get('name', student.name)
        student.education = data.get('education', student.education)
        student.skills = data.get('skills', student.skills)
        student.resume_url = data.get('resume_url', student.resume_url)
        student.experience = data.get('experience', student.experience)
        student.photo_url = data.get('photo_url', student.photo_url)
        student.location = data.get('location', student.location)
        student.linkedin = data.get('linkedin', student.linkedin)
        student.github = data.get('github', student.github)
        db.session.commit()
        return jsonify({"msg": "Profile updated successfully"}), 200

@student_bp.route('/upload_resume', methods=['POST'])
@jwt_required()
def upload_resume():
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
        
    filename = secure_filename(file.filename)
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, f"student_{student.id}_{filename}")
    file.save(file_path)
    
    # Store absolute URL (assuming backend is on localhost:5000)
    student.resume_url = f"http://127.0.0.1:5000/static/uploads/student_{student.id}_{filename}"
    db.session.commit()
    
    return jsonify({"resume_url": student.resume_url}), 200

@student_bp.route('/download_resume/<path:filename>', methods=['GET'])
def download_resume_file(filename):
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    file_path = os.path.join(upload_folder, filename)
    if os.path.exists(file_path):
        from flask import send_file
        return send_file(file_path, as_attachment=True)
    return jsonify({"msg": "File not found"}), 404

@student_bp.route('/jobs', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, make_cache_key=make_user_cache_key)
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
            "deadline": j.deadline.isoformat() if j.deadline else None,
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
                "date_applied": app.date_applied,
                "salary": job.salary,
                "skills_required": job.skills_required,
                "description": job.description
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
        cache.clear()
        return jsonify({"msg": "Application submitted successfully"}), 201

@student_bp.route('/export', methods=['POST'])
@jwt_required()
def trigger_export():
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    current_user = json.loads(get_jwt_identity())
    export_job = ExportJob(user_id=current_user['id'], status='Pending')
    db.session.add(export_job)
    db.session.commit()
    
    export_csv_task(export_job.id, current_user['id'], 'student')
    
    return jsonify({"msg": "Export task started", "job_id": export_job.id}), 202

@student_bp.route('/exports', methods=['GET'])
@jwt_required()
def get_exports():
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    current_user = json.loads(get_jwt_identity())
    jobs = ExportJob.query.filter_by(user_id=current_user['id']).order_by(ExportJob.created_at.desc()).all()
    result = [{"id": j.id, "status": j.status, "created_at": j.created_at} for j in jobs]
    return jsonify(result), 200

@student_bp.route('/exports/<int:job_id>/download', methods=['GET'])
@jwt_required()
def download_export(job_id):
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    current_user = json.loads(get_jwt_identity())
    job = ExportJob.query.filter_by(id=job_id, user_id=current_user['id']).first_or_404()
    if job.status != 'Completed' or not job.file_path:
        return jsonify({"msg": "File not ready"}), 400
        
    return send_file(os.path.abspath(job.file_path), as_attachment=True)

@student_bp.route('/applications/<int:app_id>/respond', methods=['PUT'])
@jwt_required()
def respond_offer(app_id):
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    application = Application.query.get_or_404(app_id)
    if application.student_id != student.id:
        return jsonify({"msg": "Unauthorized"}), 403
        
    data = request.get_json()
    new_status = data.get('status')
    
    if application.status != 'Offer':
        return jsonify({"msg": "Application is not in Offer status"}), 400
        
    if new_status in ['Placed', 'Rejected']:
        application.status = new_status
        job = JobPosition.query.get(application.job_id)
        company = Company.query.get(job.company_id)
        
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
                
            comp_user = User.query.get(company.user_id)
            if comp_user and comp_user.email:
                from mail import send_email
                subject = f"Offer Accepted: {student.name} for {job.title}"
                body = f"""
                <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <div style="background-color: #28a745; padding: 30px; text-align: center;">
                        <h1 style="color: white; margin: 0; font-size: 24px;">Offer Accepted</h1>
                    </div>
                    <div style="padding: 30px; background-color: #ffffff;">
                        <p style="font-size: 16px; color: #333; margin-bottom: 20px;">Dear <strong>{company.name}</strong>,</p>
                        
                        <p style="font-size: 16px; color: #555; line-height: 1.6;">
                            We are pleased to inform you that <strong>{student.name}</strong> has formally accepted your job offer for the position of <strong>{job.title}</strong>.
                        </p>
                        
                        <p style="font-size: 16px; color: #555; line-height: 1.6;">
                            The candidate's status has been successfully updated to "Placed" in your portal.
                        </p>
                        
                        <p style="font-size: 16px; color: #555; line-height: 1.6; margin-top: 30px;">
                            Best regards,<br>
                            <strong>JobFinder Placement Portal</strong>
                        </p>
                    </div>
                </div>
                """
                send_email(comp_user.email, subject, body)
                
        db.session.commit()
        return jsonify({"msg": "Offer response recorded successfully"}), 200
        
    return jsonify({"msg": "Invalid status"}), 400

from models import Message

@student_bp.route('/messages/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    applications = Application.query.filter_by(student_id=student.id).all()
    
    result = []
    for app in applications:
        job = JobPosition.query.get(app.job_id)
        company_user_id = job.company.user_id
        
        has_msg = Message.query.filter_by(application_id=app.id).first()
        if not has_msg:
            continue
            
        last_msg = Message.query.filter_by(application_id=app.id).order_by(Message.timestamp.desc()).first()
        
        result.append({
            "application_id": app.id,
            "company_name": job.company.name,
            "company_user_id": company_user_id,
            "job_title": job.title,
            "last_message": last_msg.content if last_msg else None,
            "last_timestamp": last_msg.timestamp.isoformat() if last_msg else None,
            "status": app.status
        })
    
    result.sort(key=lambda x: x['last_timestamp'] or '', reverse=True)
    return jsonify(result), 200

@student_bp.route('/messages/<int:application_id>', methods=['GET', 'POST'])
@jwt_required()
def handle_messages(application_id):
    student, err_resp, err_code = get_student_or_403()
    if err_resp: return err_resp, err_code
    
    app = Application.query.get_or_404(application_id)
    if app.student_id != student.id:
        return jsonify({"msg": "Unauthorized"}), 403
        
    job = JobPosition.query.get(app.job_id)
    company_user_id = job.company.user_id
    
    current_user = json.loads(get_jwt_identity())
    
    has_msg = Message.query.filter_by(application_id=application_id).first()
    
    if request.method == 'GET':
        if not has_msg:
            return jsonify([]), 200
            
        messages = Message.query.filter_by(application_id=application_id).order_by(Message.timestamp.asc()).all()
        result = []
        for m in messages:
            sender_name = "Unknown"
            sender_user = User.query.get(m.sender_id)
            if sender_user:
                if sender_user.role == 'student':
                    stu = Student.query.filter_by(user_id=sender_user.id).first()
                    if stu: sender_name = stu.name
                elif sender_user.role == 'company':
                    comp = Company.query.filter_by(user_id=sender_user.id).first()
                    if comp: sender_name = comp.name

            result.append({
                "id": m.id,
                "sender_id": m.sender_id,
                "sender_name": sender_name,
                "is_mine": m.sender_id == current_user['id'],
                "content": m.content,
                "timestamp": m.timestamp.isoformat()
            })
        return jsonify(result), 200
        
    if request.method == 'POST':
        if not has_msg:
            return jsonify({"msg": "You cannot start a conversation. The company must message first."}), 403
            
        data = request.get_json()
        content = data.get('content')
        if not content:
            return jsonify({"msg": "Content is required"}), 400
            
        new_msg = Message(
            sender_id=current_user['id'],
            receiver_id=company_user_id,
            application_id=application_id,
            content=content
        )
        db.session.add(new_msg)
        db.session.commit()
        
        return jsonify({
            "id": new_msg.id,
            "sender_id": new_msg.sender_id,
            "sender_name": student.name,
            "is_mine": True,
            "content": new_msg.content,
            "timestamp": new_msg.timestamp.isoformat()
        }), 201
