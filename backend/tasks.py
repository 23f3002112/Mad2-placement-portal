import csv
import os
import time
from datetime import datetime, timedelta
from celery_app import celery
from models import db, User, Student, Company, JobPosition, Application, ExportJob, Placement

# Make sure an exports directory exists
os.makedirs('exports', exist_ok=True)

@celery.task
def send_interview_reminders():
    print("--- Running Scheduled Task: Interview Reminders ---")
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    
    # Find applications with an interview scheduled within the next 24 hours
    upcoming_interviews = Application.query.filter(
        Application.status == 'Interview',
        Application.interview_date >= now,
        Application.interview_date <= tomorrow
    ).all()
    
    if not upcoming_interviews:
        print("No interviews scheduled for the next 24 hours.")
        return
        
    for app in upcoming_interviews:
        student = Student.query.get(app.student_id)
        user = User.query.get(student.user_id)
        job = JobPosition.query.get(app.job_id)
        company = Company.query.get(job.company_id)
        
        # MOCK SENDING EMAIL / SMS
        print(f"[MOCK NOTIFICATION] To: {user.email}")
        print(f"Subject: Interview Reminder - {job.title} at {company.name}")
        print(f"Body: Dear {student.name}, this is a reminder for your upcoming interview on {app.interview_date.strftime('%Y-%m-%d %H:%M')}. Good luck!")
        print("--------------------------------------------------")
        
    print(f"Sent {len(upcoming_interviews)} interview reminders.")
    return True

@celery.task
def generate_monthly_reports():
    print("--- Running Scheduled Task: Monthly Placement Reports ---")
    companies = Company.query.filter_by(is_approved=True).all()
    
    for company in companies:
        jobs = JobPosition.query.filter_by(company_id=company.id).all()
        job_ids = [j.id for j in jobs]
        
        total_apps = Application.query.filter(Application.job_id.in_(job_ids)).count() if job_ids else 0
        total_placed = Placement.query.filter_by(company_id=company.id).count()
        
        # MOCK SENDING REPORT
        user = User.query.get(company.user_id)
        print(f"[MOCK REPORT] To: {user.email}")
        print(f"Subject: Monthly Placement Analytics for {company.name}")
        print(f"Body: You had {len(jobs)} active jobs, {total_apps} total applications, and hired {total_placed} candidates this month.")
        print("--------------------------------------------------")
        
    print(f"Generated monthly reports for {len(companies)} companies.")
    return True

@celery.task
def export_csv_task(export_job_id, user_id, role):
    print(f"--- Starting CSV Export Task (Job ID: {export_job_id}) ---")
    
    export_job = ExportJob.query.get(export_job_id)
    if not export_job:
        print("Export job not found.")
        return False
        
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"export_{role}_{user_id}_{timestamp}.csv"
        filepath = os.path.join('exports', filename)
        
        # Simulate a long-running process
        time.sleep(5)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if role == 'student':
                student = Student.query.filter_by(user_id=user_id).first()
                writer.writerow(['Company', 'Job Title', 'Status', 'Date Applied', 'Interview Date', 'Feedback'])
                applications = Application.query.filter_by(student_id=student.id).all()
                for app in applications:
                    job = JobPosition.query.get(app.job_id)
                    company = Company.query.get(job.company_id)
                    writer.writerow([
                        company.name, 
                        job.title, 
                        app.status, 
                        app.date_applied.strftime('%Y-%m-%d'), 
                        app.interview_date.strftime('%Y-%m-%d %H:%M') if app.interview_date else '', 
                        app.feedback or ''
                    ])
                    
            elif role == 'company':
                company = Company.query.filter_by(user_id=user_id).first()
                writer.writerow(['Job Title', 'Student Name', 'Education', 'Skills', 'Status', 'Date Applied'])
                jobs = JobPosition.query.filter_by(company_id=company.id).all()
                for job in jobs:
                    applications = Application.query.filter_by(job_id=job.id).all()
                    for app in applications:
                        student = Student.query.get(app.student_id)
                        writer.writerow([
                            job.title,
                            student.name,
                            student.education,
                            student.skills,
                            app.status,
                            app.date_applied.strftime('%Y-%m-%d')
                        ])
                        
        export_job.file_path = filepath
        export_job.status = 'Completed'
        db.session.commit()
        print(f"Export task completed successfully. File saved to {filepath}")
        return True
        
    except Exception as e:
        print(f"Export task failed: {str(e)}")
        export_job.status = 'Failed'
        db.session.commit()
        return False
