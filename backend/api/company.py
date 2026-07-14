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
            "description": company.description,
            "website": company.website,
            "employee_count": company.employee_count,
            "founded_year": company.founded_year,
            "contact_email": company.contact_email
        }), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        company.industry = data.get('industry', company.industry)
        company.location = data.get('location', company.location)
        company.description = data.get('description', company.description)
        company.website = data.get('website', company.website)
        company.employee_count = data.get('employee_count', company.employee_count)
        company.founded_year = data.get('founded_year', company.founded_year)
        company.contact_email = data.get('contact_email', company.contact_email)
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
                "deadline": j.deadline.isoformat() if j.deadline else None,
                "created_at": j.created_at
            })
        return jsonify(result), 200
        
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        salary = data.get('salary')
        skills_required = data.get('skills_required')
        deadline_str = data.get('deadline')
        
        deadline = None
        if deadline_str:
            deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
            
        try:
            job = JobPosition(
                company_id=company.id,
                title=title,
                description=description,
                salary=salary,
                skills_required=skills_required,
                deadline=deadline,
                status='Pending'
            )
            db.session.add(job)
            db.session.commit()
            cache.clear()
            
            from models import Notification
            admin = User.query.filter_by(role='admin').first()
            if admin:
                notif = Notification(
                    user_id=admin.id,
                    title="New Job Posted",
                    message=f"Company {company.name} has posted a new job: {title}. It is pending your approval."
                )
                db.session.add(notif)
                db.session.commit()
                
            return jsonify({"msg": "Job created and pending admin approval"}), 201
        except Exception as e:
            import traceback
            return jsonify({"msg": str(e), "trace": traceback.format_exc()}), 500

from mail import send_email

@company_bp.route('/jobs/<int:job_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def handle_single_job(job_id):
    company, err_resp, err_code = get_company_or_403()
    if err_resp: return err_resp, err_code
    
    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first_or_404()
    
    if request.method == 'DELETE':
        Application.query.filter_by(job_id=job.id).delete()
        db.session.delete(job)
        db.session.commit()
        cache.clear()
        return jsonify({"msg": "Job deleted successfully"}), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        
        job.title = data.get('title', job.title)
        job.description = data.get('description', job.description)
        job.salary = data.get('salary', job.salary)
        job.skills_required = data.get('skills_required', job.skills_required)
        
        deadline_str = data.get('deadline')
        if deadline_str:
            job.deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
            
        db.session.commit()
        cache.clear()
        
        # Send email to all students who applied
        applications = Application.query.filter_by(job_id=job.id).all()
        for app in applications:
            student = Student.query.get(app.student_id)
            user = User.query.get(student.user_id)
            if user:
                subject = f"Update on your application for {job.title}"
                body = f"Hello {student.name},\n\nThe company {company.name} has recently updated the job details for '{job.title}'.\nPlease check the portal for any new requirements, deadlines, or changes.\n\nBest,\nPlacement Portal Team"
                send_email(user.email, subject, body)
                
        return jsonify({"msg": "Job updated successfully and applicants notified"}), 200

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
            "interview_type": app.interview_type,
            "interview_location_or_link": app.interview_location_or_link,
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
    interview_type = data.get('interview_type')
    interview_location_or_link = data.get('interview_location_or_link')
    
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
    if interview_type:
        application.interview_type = interview_type
    if interview_location_or_link:
        application.interview_location_or_link = interview_location_or_link
        
    if new_status == 'Interview' and interview_date:
        student = Student.query.get(application.student_id)
        user = User.query.get(student.user_id)
        if user and user.email:
            from mail import send_email
            
            interview_date_obj = datetime.fromisoformat(interview_date.replace('Z', '+00:00'))
            date_str = interview_date_obj.strftime("%A, %B %d, %Y at %I:%M %p")
            
            loc_label = "Google Meet Link" if interview_type == 'Online' else "Location"
            
            subject = f"Interview Invitation for {job.title} at {company.name}"
            body = f"""
            <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <div style="background-color: #00008b; padding: 30px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 24px;">Interview Invitation</h1>
                </div>
                <div style="padding: 30px; background-color: #ffffff;">
                    <p style="font-size: 16px; color: #333; margin-bottom: 20px;">Dear <strong>{student.name}</strong>,</p>
                    
                    <p style="font-size: 16px; color: #555; line-height: 1.6;">
                        Congratulations! We are excited to invite you to an interview for the <strong>{job.title}</strong> position at <strong>{company.name}</strong>.
                    </p>
                    
                    <div style="background-color: #f8f9fa; border-left: 4px solid #00008b; padding: 20px; margin: 25px 0; border-radius: 4px;">
                        <h3 style="margin-top: 0; color: #00008b; font-size: 18px;">Interview Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px 0; color: #666; width: 30%;"><strong>Date & Time:</strong></td>
                                <td style="padding: 8px 0; color: #333;">{date_str}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>Type:</strong></td>
                                <td style="padding: 8px 0; color: #333;">{interview_type or 'Online'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>{loc_label}:</strong></td>
                                <td style="padding: 8px 0; color: #333;">{interview_location_or_link or 'TBD'}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p style="font-size: 16px; color: #555; line-height: 1.6;">
                        Please make sure to be on time and prepared. If you have any questions, you can reply directly to the company through the placement portal messaging system.
                    </p>
                    
                    <p style="font-size: 16px; color: #555; line-height: 1.6; margin-top: 30px;">
                        Best regards,<br>
                        <strong>{company.name} Team</strong>
                    </p>
                </div>
                <div style="background-color: #f4f6f9; padding: 15px; text-align: center; border-top: 1px solid #eee;">
                    <p style="font-size: 12px; color: #999; margin: 0;">Powered by JobFinder Placement Portal</p>
                </div>
            </div>
            """
            send_email(user.email, subject, body)
            
    if new_status == 'Offer':
        joining_date = data.get('joining_date')
        student = Student.query.get(application.student_id)
        user = User.query.get(student.user_id)
        if user and user.email and joining_date:
            from mail import send_email
            
            join_date_obj = datetime.strptime(joining_date, "%Y-%m-%d")
            join_date_str = join_date_obj.strftime("%A, %B %d, %Y")
            
            subject = f"Job Offer: {job.title} at {company.name}"
            body = f"""
            <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <div style="background-color: #00008b; padding: 30px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 24px;">Offer Letter</h1>
                </div>
                <div style="padding: 30px; background-color: #ffffff;">
                    <p style="font-size: 16px; color: #333; margin-bottom: 20px;">Dear <strong>{student.name}</strong>,</p>
                    
                    <p style="font-size: 16px; color: #555; line-height: 1.6;">
                        Congratulations! After a successful interview process, we are thrilled to offer you the position of <strong>{job.title}</strong> at <strong>{company.name}</strong>.
                    </p>
                    
                    <p style="font-size: 16px; color: #555; line-height: 1.6;">
                        We were very impressed with your background and skills, and we believe you will be a fantastic addition to our team.
                    </p>
                    
                    <div style="background-color: #f8f9fa; border-left: 4px solid #28a745; padding: 20px; margin: 25px 0; border-radius: 4px;">
                        <h3 style="margin-top: 0; color: #28a745; font-size: 18px;">Offer Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px 0; color: #666; width: 40%;"><strong>Job Title:</strong></td>
                                <td style="padding: 8px 0; color: #333;">{job.title}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>Expected Joining Date:</strong></td>
                                <td style="padding: 8px 0; color: #333;">{join_date_str}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p style="font-size: 16px; color: #555; line-height: 1.6;">
                        Please confirm your acceptance of this offer by replying to the company via the placement portal. We look forward to welcoming you aboard!
                    </p>
                    
                    <p style="font-size: 16px; color: #555; line-height: 1.6; margin-top: 30px;">
                        Warm welcome,<br>
                        <strong>{company.name} Team</strong>
                    </p>
                </div>
                <div style="background-color: #f4f6f9; padding: 15px; text-align: center; border-top: 1px solid #eee;">
                    <p style="font-size: 12px; color: #999; margin: 0;">Powered by JobFinder Placement Portal</p>
                </div>
            </div>
            """
            send_email(user.email, subject, body)
        
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
            "sender_name": company.name,
            "is_mine": True,
            "content": new_msg.content,
            "timestamp": new_msg.timestamp.isoformat()
        }), 201
