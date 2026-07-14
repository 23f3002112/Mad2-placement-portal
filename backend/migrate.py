import sqlite3

def run_migration():
    conn = sqlite3.connect('instance/ppa.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE student ADD COLUMN photo_url VARCHAR(255)")
        print("Added photo_url")
    except Exception as e:
        print("photo_url:", e)
        
    try:
        cursor.execute("ALTER TABLE student ADD COLUMN location VARCHAR(100)")
        print("Added location")
    except Exception as e:
        print("location:", e)
        
    try:
        cursor.execute("ALTER TABLE student ADD COLUMN linkedin VARCHAR(255)")
        print("Added linkedin")
    except Exception as e:
        print("linkedin:", e)
        
    try:
        cursor.execute("ALTER TABLE student ADD COLUMN github VARCHAR(255)")
        print("Added github")
    except Exception as e:
        print("github:", e)
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    run_migration()
