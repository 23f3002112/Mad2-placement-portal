import sqlite3

def run_migration():
    conn = sqlite3.connect('instance/ppa.db')
    cursor = conn.cursor()
    
    columns = [
        "website VARCHAR(255)",
        "employee_count VARCHAR(50)",
        "founded_year VARCHAR(10)",
        "contact_email VARCHAR(120)"
    ]
    
    for col in columns:
        try:
            cursor.execute(f"ALTER TABLE company ADD COLUMN {col}")
            print(f"Added {col}")
        except Exception as e:
            print(f"Failed to add {col}: {e}")
            
    conn.commit()
    conn.close()

if __name__ == '__main__':
    run_migration()
