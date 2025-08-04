import sqlite3
import os

def create_database():
    """Create SQLite database with users and projects tables"""
    
    db_path = "data.db"
    
    if os.path.exists(db_path):
        print(f"Database {db_path} already exists. Connecting to existing database...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                skills TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                tags TEXT
            )
        ''')
        
        conn.commit()
        print(f"Database '{db_path}' created successfully!")
        print("Tables created:")
        print("- users (id, name, email, password, skills)")
        print("- projects (id, title, description, tags)")
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"\nTables in database: {[table[0] for table in tables]}")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        
        conn.close()

def insert_sample_data():
    """Insert 3 sample users and 3 sample projects into data.db"""
    
   
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    print("Connected to data.db database")
    
    try:
        
        users = [
            ("Alice Johnson", "alice@email.com", "password123", "python, marketing"),
            ("Bob Chen", "bob@email.com", "securepass456", "javascript, design, photography"),
            ("Carol Davis", "carol@email.com", "mypass789", "data analysis, sql, python")
        ]
        
        print("\nInserting users...")
        for user in users:
            cursor.execute('''
                INSERT OR IGNORE INTO users (name, email, password, skills)
                VALUES (?, ?, ?, ?)
            ''', user)
            print(f"  Added user: {user[0]} with skills: {user[3]}")
        
        projects = [
            ("Personal Blog", "A simple blog website built with modern web technologies", "python, web, blog"),
            ("Data Dashboard", "Interactive dashboard for visualizing sales data", "data analysis, visualization"),
            ("Mobile Game", "Fun puzzle game for smartphones", "mobile, game, design")
        ]
        
        print("\nInserting projects...")
        for project in projects:
            cursor.execute('''
                INSERT OR IGNORE INTO projects (title, description, tags)
                VALUES (?, ?, ?)
            ''', project)
            print(f"  Added project: {project[0]} with tags: {project[2]}")
        
        conn.commit()
        print("\nAll data inserted successfully!")
        
        print("\n--- Users in database ---")
        cursor.execute("SELECT id, name, email, skills FROM users")
        all_users = cursor.fetchall()
        for user in all_users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Skills: {user[3]}")
        
        print("\n--- Projects in database ---")
        cursor.execute("SELECT id, title, description, tags FROM projects")
        all_projects = cursor.fetchall()
        for project in all_projects:
            print(f"ID: {project[0]}, Title: {project[1]}")
            print(f"    Description: {project[2]}")
            print(f"    Tags: {project[3]}\n")
    
    except sqlite3.IntegrityError as e:
        print(f"Error: Could not insert data. {e}")
        print("(This might happen if you run the script multiple times)")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        conn.close()
        print("Database connection closed.")


def match_projects_for_user(user_id):
    """
    Find the top 3 projects that best match a user's skills.
    
    Args:
        user_id (int): The ID of the user to find matches for
    
    Returns:
        list: Top 3 matching projects with match details, or empty list if no matches
              Format: [
                  {
                      'project_id': int,
                      'title': str,
                      'description': str,
                      'tags': str,
                      'match_count': int,
                      'matched_skills': list
                  }
              ]
    """
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("SELECT name, skills FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return []
        
        user_name, user_skills = user_data
        
        if not user_skills:
            return []
        
        user_skills_set = set()
        for skill in user_skills.split(','):
            user_skills_set.add(skill.strip().lower())
        
        cursor.execute("SELECT id, title, description, tags FROM projects")
        all_projects = cursor.fetchall()
        
        if not all_projects:
            return []
        
        project_matches = []
        
        for project in all_projects:
            project_id, title, description, tags = project
            
            project_tags_set = set()
            if tags:  
                for tag in tags.split(','):
                    project_tags_set.add(tag.strip().lower())
            
            matched_skills = user_skills_set.intersection(project_tags_set)
            match_count = len(matched_skills)
            
            if match_count > 0:
                project_match = {
                    'project_id': project_id,
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'match_count': match_count,
                    'matched_skills': list(matched_skills)  
                }
                project_matches.append(project_match)
        
        project_matches.sort(key=lambda x: (-x['match_count'], x['title']))
        return project_matches[:3]
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    
    finally:
        conn.close()

def get_user_info(user_id):
    """Get user name and skills for display"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name, skills FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        return result if result else (None, None)
    except sqlite3.Error:
        return (None, None)
    finally:
        conn.close()

def display_recommendations(user_id):
    """Display project recommendations for a user"""
    
    user_name, user_skills = get_user_info(user_id)
    
    if not user_name:
        print(f"User with ID {user_id} not found!")
        return
    
    print("=" * 60)
    print(f"PROJECT RECOMMENDATIONS FOR: {user_name}")
    print(f"User Skills: {user_skills}")
    print("=" * 60)
    
    matches = match_projects_for_user(user_id)
    
    if not matches:
        print("No matching projects found!")
        print("Try adding more skills or check if there are projects in the database.")
        return
    
    print(f"\n🎯 Found {len(matches)} matching projects:\n")
    
    for i, match in enumerate(matches, 1):
        print(f"#{i} - {match['title']}")
        print("-" * 40)
        print(f"Description: {match['description']}")
        print(f"Matching Tags: {match['matched_skills']}")
        print(f"Score: {match['match_count']} out of {len(match['tags'].split(',')) if match['tags'] else 0} tags")
        print()

def show_all_users():
    """Display all users in the database"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name, skills FROM users")
        users = cursor.fetchall()
        
        print("\n" + "=" * 60)
        print("ALL USERS IN DATABASE:")
        print("=" * 60)
        
        if users:
            for user in users:
                print(f"ID {user[0]}: {user[1]} - Skills: {user[2]}")
        else:
            print("No users found in database")
    
    except sqlite3.Error as e:
        print(f"Error reading users: {e}")
    
    finally:
        conn.close()

def show_all_projects():
    """Display all projects in the database"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, title, description, tags FROM projects")
        projects = cursor.fetchall()
        
        print("\n" + "=" * 60)
        print("ALL PROJECTS IN DATABASE:")
        print("=" * 60)
        
        if projects:
            for project in projects:
                print(f"ID {project[0]}: {project[1]}")
                print(f"    Description: {project[2]}")
                print(f"    Tags: {project[3]}\n")
        else:
            print("No projects found in database")
    
    except sqlite3.Error as e:
        print(f"Error reading projects: {e}")
    
    finally:
        conn.close()

def check_database_exists():
    """Check if data.db exists"""
    return os.path.exists('data.db')


def demo_all_users():
    """Demonstrate the matching function with all users in the database"""
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("SELECT id, name FROM users")
        users = cursor.fetchall()
        
        print("=== PROJECT MATCHING DEMO FOR ALL USERS ===\n")
        
        for user_id, name in users:
            print(f"{'='*50}")
            print(f"RECOMMENDATIONS FOR: {name} (ID: {user_id})")
            print(f"{'='*50}")
            
            
            matches = match_projects_for_user(user_id)
            
            if matches:
                print(f"Found {len(matches)} matching projects!")
                for i, match in enumerate(matches, 1):
                    print(f"  {i}. {match['title']} - Score: {match['match_count']}")
                    print(f"     Matched skills: {match['matched_skills']}")
            else:
                print("No matching projects found.")
            
            print("\n")
    
    except sqlite3.Error as e:
        print(f" Database error: {e}")
    
    finally:
        conn.close()

def interactive_menu():
    """Interactive menu system for the application"""
    
    while True:
        print("\n" + "=" * 50)
        print("PROJECT MATCHING SYSTEM")
        print("=" * 50)
        print("1. Setup Database (create tables)")
        print("2. Insert Sample Data")
        print("3. Show All Users")
        print("4. Show All Projects")
        print("5. Get Recommendations for User")
        print("6. Demo All Users")
        print("7. Quick Test (User ID 1)")
        print("0. Exit")
        print("-" * 50)
        
        try:
            choice = input("Enter your choice (0-7): ").strip()
            
            if choice == "0":
                print("Goodbye!")
                break
            
            elif choice == "1":
                print("\n🔧 Setting up database...")
                create_database()
            
            elif choice == "2":
                if not check_database_exists():
                    print("Database not found! Please create database first (option 1)")
                    continue
                print("\nInserting sample data...")
                insert_sample_data()
            
            elif choice == "3":
                if not check_database_exists():
                    print("Database not found! Please create database first (option 1)")
                    continue
                show_all_users()
            
            elif choice == "4":
                if not check_database_exists():
                    print("Database not found! Please create database first (option 1)")
                    continue
                show_all_projects()
            
            elif choice == "5":
                if not check_database_exists():
                    print("Database not found! Please create database first (option 1)")
                    continue
                try:
                    user_id = int(input("Enter user ID: "))
                    print(f"\nGetting recommendations for user ID {user_id}...")
                    display_recommendations(user_id)
                except ValueError:
                    print("Please enter a valid number")
            
            elif choice == "6":
                if not check_database_exists():
                    print("Database not found! Please create database first (option 1)")
                    continue
                print("\nRunning demo for all users...")
                demo_all_users()
            
            elif choice == "7":
                if not check_database_exists():
                    print("Database not found! Please create database first (option 1)")
                    continue
                print("\n⚡ Quick test with user ID 1...")
                display_recommendations(1)
            
            else:
                print("Invalid choice! Please enter 0-7")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def quick_setup_and_test():
    """Quick setup and test function for immediate use"""
    
    print("QUICK SETUP AND TEST")
    print("=" * 40)
    
    print("Step 1: Creating database...")
    create_database()
    
    print("\nStep 2: Inserting sample data...")
    insert_sample_data()
    
    print("\nStep 3: Testing recommendations...")
    display_recommendations(1)
    
    show_all_users()

if __name__ == "__main__":
    print("COMPLETE PROJECT MATCHING SYSTEM")
    print("=" * 50)
    
    if not check_database_exists():
        print("Database not found. Running quick setup...")
        quick_setup_and_test()
    else:
        print("Database found!")
        
        print("\nRunning quick test with user ID 1...")
        display_recommendations(1)
    
    print("\n" + "=" * 50)
    print("Starting interactive menu...")
    interactive_menu()
