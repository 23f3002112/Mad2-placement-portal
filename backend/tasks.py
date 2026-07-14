import csv
import os
import time
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from celery_app import celery
from models import db, User, Student, Company, JobPosition, Application, ExportJob, Placement, Notification
from mail import send_email

# Make sure an exports directory exists
os.makedirs('exports', exist_ok=True)

def send_notification(user_id, title, message, attachment_path=None):
    # Instead of real emails, we insert a notification into the DB
    # If there is a PDF attachment, we can append a link to it in the message
    if attachment_path:
        filename = os.path.basename(attachment_path)
        message += f'<br><br><a href="/api/downloads/{filename}" class="btn btn-sm btn-outline-primary" target="_blank">Download Report</a>'
        
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message
    )
    db.session.add(notification)
    db.session.commit()
    print(f"[NOTIFICATION] Sent to User ID {user_id}: {title}")
    return True

def generate_pdf_report(company_name, jobs, total_apps, total_placed, filename):
    filepath = os.path.join('exports', filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"Monthly Placement Analytics: {company_name}")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 710, f"Active Jobs Posted: {jobs}")
    c.drawString(100, 680, f"Total Applications Received: {total_apps}")
    c.drawString(100, 650, f"Total Candidates Placed: {total_placed}")
    c.drawString(100, 620, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    c.save()
    return filepath

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
        
        subject = f"Interview Reminder - {job.title} at {company.name}"
        body = f"""
        <html>
            <body>
                <h2>Interview Reminder</h2>
                <p>Dear {student.name},</p>
                <p>This is a reminder for your upcoming interview for the <b>{job.title}</b> position at <b>{company.name}</b>.</p>
                <p><b>Date & Time:</b> {app.interview_date.strftime('%Y-%m-%d %H:%M')}</p>
                <p>Good luck!</p>
            </body>
        </html>
        """
        send_notification(user.id, subject, body)
        send_email(user.email, subject, body)
        
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
        
        user = User.query.get(company.user_id)
        
        # Generate PDF
        pdf_filename = f"report_{company.id}_{datetime.now().strftime('%Y%m')}.pdf"
        pdf_path = generate_pdf_report(company.name, len(jobs), total_apps, total_placed, pdf_filename)
        
        # Send Email
        subject = f"Monthly Placement Analytics for {company.name}"
        body = f"""
        <html>
            <body>
                <h2>Monthly Analytics Report</h2>
                <p>Dear {company.name} team,</p>
                <p>Please find attached your monthly placement analytics report.</p>
                <p>Thank you for partnering with JobFinder.</p>
            </body>
        </html>
        """
        send_notification(user.id, subject, body, attachment_path=pdf_path)
        send_email(user.email, subject, body, attachment_file=pdf_path)
        
    print(f"Generated and sent monthly reports for {len(companies)} companies.")
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
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if role == 'student':
                student = Student.query.filter_by(user_id=user_id).first()
                writer.writerow(['Company', 'Job Title', 'Status', 'Date Applied', 'Interview Date', 'Feedback'])
                applications = Application.query.filter_by(student_id=student.id).all()
                for app in applications:
                    job = JobPosition.query.get(app.job_id)
                    company = Company.query.get(job.company_id)
                    local_date_applied = app.date_applied + timedelta(hours=5, minutes=30)
                    local_interview_date = app.interview_date + timedelta(hours=5, minutes=30) if app.interview_date else None
                    writer.writerow([
                        company.name, 
                        job.title, 
                        app.status, 
                        local_date_applied.strftime('%Y-%m-%d'), 
                        local_interview_date.strftime('%Y-%m-%d %H:%M') if local_interview_date else '', 
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
                        local_date_applied = app.date_applied + timedelta(hours=5, minutes=30)
                        writer.writerow([
                            job.title,
                            student.name,
                            student.education,
                            student.skills,
                            app.status,
                            local_date_applied.strftime('%Y-%m-%d')
                        ])
                        
        export_job.file_path = filepath
        export_job.status = 'Completed'
        db.session.commit()
        
        user = User.query.get(user_id)
        if user and user.email:
            # Read CSV to format as HTML table
            table_html = "<table border='1' style='border-collapse: collapse; width: 100%; text-align: left;'>"
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                lines = list(reader)
                if lines:
                    headers = lines[0]
                    table_html += "<tr>" + "".join([f"<th style='padding: 8px; background-color: #f2f2f2;'>{h}</th>" for h in headers]) + "</tr>"
                    for row in lines[1:]:
                        table_html += "<tr>" + "".join([f"<td style='padding: 8px;'>{c}</td>" for c in row]) + "</tr>"
            table_html += "</table>"

            subject = "Your Data Export is Ready"
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2>Data Export Complete</h2>
                    <p>Dear User,</p>
                    <p>Your requested data export has been completed successfully. Here is your data:</p>
                    <div style="margin: 20px 0; overflow-x: auto;">
                        {table_html}
                    </div>
                    <p>The CSV file is also attached to this email.</p>
                    <p>Thank you for using JobFinder.</p>
                </body>
            </html>
            """
            send_email(user.email, subject, body, attachment_file=filepath)
            send_notification(user.id, subject, "Your data export is ready. Check your email or download it here.", attachment_path=filepath)
            
        print(f"Export task completed successfully. File saved to {filepath}")
        return True
        
    except Exception as e:
        print(f"Export task failed: {str(e)}")
        export_job.status = 'Failed'
        db.session.commit()
        return False
