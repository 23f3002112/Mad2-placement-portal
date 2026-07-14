import sqlite3

def run_migration():
    conn = sqlite3.connect('instance/ppa.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE application ADD COLUMN interview_type VARCHAR(20)")
        print("Added interview_type to application")
    except sqlite3.OperationalError as e:
        print(f"Error (might already exist): {e}")

    try:
        cursor.execute("ALTER TABLE application ADD COLUMN interview_location_or_link VARCHAR(255)")
        print("Added interview_location_or_link to application")
    except sqlite3.OperationalError as e:
        print(f"Error (might already exist): {e}")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    run_migration()
