from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'company', 'student'
    active = db.Column(db.Boolean, default=True)

class Company(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    employee_count = db.Column(db.String(50))
    founded_year = db.Column(db.String(10))
    contact_email = db.Column(db.String(120))
    is_approved = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref=db.backref('company_profile', uselist=False))

class Student(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    education = db.Column(db.String(200))
    skills = db.Column(db.String(200))
    resume_url = db.Column(db.String(255))
    experience = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    location = db.Column(db.String(100))
    linkedin = db.Column(db.String(255))
    github = db.Column(db.String(255))
    
    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))

class JobPosition(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    salary = db.Column(db.String(50))
    skills_required = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Pending') # 'Pending', 'Approved', 'Closed', 'Rejected'
    deadline = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    company = db.relationship('Company', backref=db.backref('job_positions', lazy=True))

class Application(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_position.id'), nullable=False)
    status = db.Column(db.String(20), default='Applied') # Applied, Shortlisted, Selected, Rejected, Interview
    feedback = db.Column(db.Text)
    interview_date = db.Column(db.DateTime)
    interview_type = db.Column(db.String(20)) # 'Online', 'In-Person'
    interview_location_or_link = db.Column(db.String(255))
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('Student', backref=db.backref('applications', lazy=True))
    job = db.relationship('JobPosition', backref=db.backref('applications', lazy=True))

class Placement(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_position.id'), nullable=False)
    position_offered = db.Column(db.String(100))
    salary_offered = db.Column(db.String(50))
    joining_date = db.Column(db.Date)
    
    student = db.relationship('Student', backref=db.backref('placements', lazy=True))
    company = db.relationship('Company', backref=db.backref('placements', lazy=True))
    job = db.relationship('JobPosition', backref=db.backref('placement_record', uselist=False))

class ExportJob(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Completed, Failed
    file_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('export_jobs', lazy=True))

class Notification(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('notifications', lazy=True, order_by='Notification.created_at.desc()'))

class Message(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    application = db.relationship('Application')
