import sqlite3
from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

def run_migrations():
    conn = sqlite3.connect('instance/ppa.db')
    cursor = conn.cursor()
    
    print("Running database migrations...")
    
    # Student migrations
    student_columns = [
        "photo_url VARCHAR(255)",
        "location VARCHAR(100)",
        "linkedin VARCHAR(255)",
        "github VARCHAR(255)"
    ]
    for col in student_columns:
        try:
            cursor.execute(f"ALTER TABLE student ADD COLUMN {col}")
            print(f"Added {col} to student")
        except sqlite3.OperationalError:
            pass

    # Application migrations
    app_columns = [
        "interview_type VARCHAR(20)",
        "interview_location_or_link VARCHAR(255)"
    ]
    for col in app_columns:
        try:
            cursor.execute(f"ALTER TABLE application ADD COLUMN {col}")
            print(f"Added {col} to application")
        except sqlite3.OperationalError:
            pass

    # Company migrations
    company_columns = [
        "website VARCHAR(255)",
        "employee_count VARCHAR(50)",
        "founded_year VARCHAR(10)",
        "contact_email VARCHAR(120)"
    ]
    for col in company_columns:
        try:
            cursor.execute(f"ALTER TABLE company ADD COLUMN {col}")
            print(f"Added {col} to company")
        except sqlite3.OperationalError:
            pass

    # Job Position migrations
    try:
        cursor.execute("ALTER TABLE job_position ADD COLUMN deadline DATETIME")
        print("Added deadline to job_position")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()
    print("Migrations completed.")

def setup():
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        run_migrations()
        
        admin_email = 'admin@institute.com'
        admin_exists = User.query.filter_by(email=admin_email).first()
        
        if not admin_exists:
            print("Creating Admin user...")
            hashed_pw = generate_password_hash('111')
            admin_user = User(email=admin_email, password=hashed_pw, role='admin', active=True)
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user {admin_email} created successfully.")
        else:
            print(f"Admin user {admin_email} already exists.")
            
if __name__ == '__main__':
    setup()
