import sqlite3

def run_migration():
    conn = sqlite3.connect('instance/ppa.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE job_position ADD COLUMN deadline DATETIME")
        print("Added deadline to job_position")
    except Exception as e:
        print(f"Failed to add deadline: {e}")
            
    conn.commit()
    conn.close()

if __name__ == '__main__':
    run_migration()
