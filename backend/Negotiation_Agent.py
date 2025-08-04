import sqlite3
import sys
import os

def update_projects_table():
    """
    Update the projects table to include new columns:
    - expected_budget (INTEGER)
    - expected_timeline_days (INTEGER)
    - expected_deliverables (TEXT)
    """
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='projects'
        """)
        
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            print("Projects table exists. Checking for new columns...")
            
            cursor.execute("PRAGMA table_info(projects)")
            columns = [column[1] for column in cursor.fetchall()]
            
            new_columns = [
                ('expected_budget', 'INTEGER'),
                ('expected_timeline_days', 'INTEGER'),
                ('expected_deliverables', 'TEXT')
            ]
            
            for column_name, column_type in new_columns:
                if column_name not in columns:
                    cursor.execute(f"ALTER TABLE projects ADD COLUMN {column_name} {column_type}")
                    print(f"Added column: {column_name}")
                else:
                    print(f"Column {column_name} already exists")
        
        else:
            print("Projects table doesn't exist. Creating new table...")
            
            cursor.execute("""
                CREATE TABLE projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    created_date DATE DEFAULT CURRENT_DATE,
                    expected_budget INTEGER,
                    expected_timeline_days INTEGER,
                    expected_deliverables TEXT
                )
            """)
            print("Created projects table with new schema")
        
        conn.commit()
        print("Projects table updated successfully!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def create_proposals_table():
    """
    Create a proposals table with the following fields:
    - id (INTEGER PRIMARY KEY)
    - project_id (INTEGER)
    - client_id (INTEGER)
    - proposed_budget (INTEGER)
    - proposed_timeline_days (INTEGER)
    - proposed_deliverables (TEXT)
    """
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='proposals'
        """)
        
        if cursor.fetchone():
            print("Proposals table already exists!")
        
        else:
            cursor.execute("""
                CREATE TABLE proposals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    client_id INTEGER,
                    proposed_budget INTEGER,
                    proposed_timeline_days INTEGER,
                    proposed_deliverables TEXT,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id),
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            """)
            
            print("Created proposals table successfully!")
            conn.commit()
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def setup_database():
    """Initialize database with all required tables"""
    print("Setting up database...")
    update_projects_table()
    create_proposals_table()
    print("Database setup complete!\n")

def insert_sample_data():
    """Insert sample data for testing"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT
            )
        """)
        
        cursor.execute("SELECT COUNT(*) FROM clients")
        if cursor.fetchone()[0] == 0:
            sample_clients = [
                ("TechCorp Ltd", "contact@techcorp.com"),
                ("StartupXYZ", "hello@startupxyz.com"),
                ("BigBusiness Inc", "projects@bigbusiness.com")
            ]
            cursor.executemany("INSERT INTO clients (name, email) VALUES (?, ?)", sample_clients)
            print("Inserted sample clients")
        
        
        cursor.execute("SELECT COUNT(*) FROM projects")
        if cursor.fetchone()[0] == 0:
            sample_projects = [
                ("E-commerce Website", "Complete online store with payment integration", "active", 75000, 120, "Website, Mobile app, Admin panel, Payment gateway"),
                ("Mobile App Development", "iOS and Android app for food delivery", "pending", 100000, 180, "iOS app, Android app, Backend API, Admin dashboard"),
                ("Brand Identity Design", "Logo and brand guidelines for startup", "pending", 25000, 45, "Logo design, Brand guidelines, Business cards, Letterhead")
            ]
            cursor.executemany("""
                INSERT INTO projects (name, description, status, expected_budget, expected_timeline_days, expected_deliverables)
                VALUES (?, ?, ?, ?, ?, ?)
            """, sample_projects)
            print("Inserted sample projects")
        
        
        cursor.execute("SELECT COUNT(*) FROM proposals")
        if cursor.fetchone()[0] == 0:
            sample_proposals = [
                (1, 1, 82000, 110, "Website, Mobile app, Admin panel, Payment gateway, SEO optimization"),
                (1, 2, 70000, 135, "Website, Mobile app, Basic admin panel"),
                (2, 1, 95000, 160, "iOS app, Android app, Backend API, Admin dashboard"),
                (2, 3, 120000, 200, "iOS app, Android app, Backend API, Advanced admin dashboard, Analytics"),
                (3, 2, 22000, 40, "Logo design, Basic brand guidelines, Business cards")
            ]
            cursor.executemany("""
                INSERT INTO proposals (project_id, client_id, proposed_budget, proposed_timeline_days, proposed_deliverables)
                VALUES (?, ?, ?, ?, ?)
            """, sample_proposals)
            print("Inserted sample proposals")
        
        conn.commit()
        print("Sample data inserted successfully!\n")
    
    except sqlite3.Error as e:
        print(f"Error inserting sample data: {e}")
        conn.rollback()
    
    finally:
        conn.close()


def negotiate_project(project_id, client_id):
    """
    Compare project expectations with client proposal and determine negotiation status.
    
    Args:
        project_id (int): ID of the project
        client_id (int): ID of the client
    
    Returns:
        dict: Negotiation results with status, suggestions, and counteroffers
    """
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("""
            SELECT expected_budget, expected_timeline_days, expected_deliverables, name
            FROM projects 
            WHERE id = ?
        """, (project_id,))
        
        project_data = cursor.fetchone()
        if not project_data:
            return {"error": f"Project {project_id} not found"}
        
        expected_budget, expected_timeline, expected_deliverables, project_name = project_data
        
        cursor.execute("""
            SELECT proposed_budget, proposed_timeline_days, proposed_deliverables
            FROM proposals 
            WHERE project_id = ? AND client_id = ?
            ORDER BY created_date DESC
            LIMIT 1
        """, (project_id, client_id))
        
        proposal_data = cursor.fetchone()
        if not proposal_data:
            return {"error": f"No proposal found for project {project_id} and client {client_id}"}
        
        proposed_budget, proposed_timeline, proposed_deliverables = proposal_data
        
        def get_status_and_counteroffer(expected, proposed):
            if expected is None or proposed is None:
                return "Cannot Compare", None
            
            if expected == 0:
                difference_percent = float('inf') if proposed != 0 else 0
            else:
                difference_percent = abs((proposed - expected) / expected) * 100
            
            counteroffer = None
            
            if difference_percent <= 10:
                status = "Accepted"
            elif difference_percent <= 25:
                status = "Needs Revision"
                
                counteroffer = int((expected + proposed) / 2)
            else:
                status = "Rejected"
            
            return status, counteroffer
        
        budget_status, budget_counteroffer = get_status_and_counteroffer(expected_budget, proposed_budget)
        timeline_status, timeline_counteroffer = get_status_and_counteroffer(expected_timeline, proposed_timeline)
        
        deliverables_counteroffer = None
        if isinstance(expected_deliverables, str) and isinstance(proposed_deliverables, str):
            deliverables_status = "Accepted" if expected_deliverables.lower().strip() == proposed_deliverables.lower().strip() else "Needs Revision"
        else:
            try:
                expected_del_num = int(expected_deliverables) if expected_deliverables else None
                proposed_del_num = int(proposed_deliverables) if proposed_deliverables else None
                deliverables_status, deliverables_counteroffer = get_status_and_counteroffer(expected_del_num, proposed_del_num)
            except (ValueError, TypeError):
                deliverables_status = "Cannot Compare"
        
        statuses = [budget_status, timeline_status, deliverables_status]
        
        if all(status == "Accepted" for status in statuses):
            overall_status = "Accepted"
        elif any(status == "Rejected" for status in statuses):
            overall_status = "Rejected"
        elif any(status == "Cannot Compare" for status in statuses):
            overall_status = "Needs Review"
        else:
            overall_status = "Needs Revision"
        
        return {
            "project_id": project_id,
            "client_id": client_id,
            "project_name": project_name,
            "overall_status": overall_status,
            "budget": {
                "status": budget_status,
                "expected": expected_budget,
                "proposed": proposed_budget,
                "counteroffer": budget_counteroffer
            },
            "timeline": {
                "status": timeline_status,
                "expected": expected_timeline,
                "proposed": proposed_timeline,
                "counteroffer": timeline_counteroffer
            },
            "deliverables": {
                "status": deliverables_status,
                "expected": expected_deliverables,
                "proposed": proposed_deliverables,
                "counteroffer": deliverables_counteroffer
            },
            "summary": f"Project {overall_status.lower()} - {sum(1 for s in statuses if s == 'Accepted')}/3 fields accepted"
        }
    
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}
    
    finally:
        conn.close()

def format_currency(amount):
    """Format amount with rupee symbol"""
    if amount is None:
        return "Not specified"
    return f"₹{amount:,}"

def print_negotiation_results(project_id, client_id):
    """Print negotiation results in the specified format"""
    
    results = negotiate_project(project_id, client_id)
    
    if "error" in results:
        print(f"Error: {results['error']}")
        return
    
    budget = results["budget"]
    if budget["status"] == "Needs Revision" and budget["expected"] and budget["proposed"]:
        counteroffer_text = f", Counteroffer: {format_currency(budget['counteroffer'])}" if budget["counteroffer"] else ""
        print(f"Budget: {budget['status']} (Expected: {format_currency(budget['expected'])}, Proposed: {format_currency(budget['proposed'])}{counteroffer_text})")
    elif budget["status"] == "Rejected" and budget["expected"] and budget["proposed"]:
        print(f"Budget: {budget['status']} (Expected: {format_currency(budget['expected'])}, Proposed: {format_currency(budget['proposed'])})")
    else:
        print(f"Budget: {budget['status']}")
    
    timeline = results["timeline"]
    if timeline["status"] == "Needs Revision" and timeline["expected"] and timeline["proposed"]:
        counteroffer_text = f", Counteroffer: {timeline['counteroffer']} days" if timeline["counteroffer"] else ""
        print(f"Timeline: {timeline['status']} (Expected: {timeline['expected']} days, Proposed: {timeline['proposed']} days{counteroffer_text})")
    elif timeline["status"] == "Rejected" and timeline["expected"] and timeline["proposed"]:
        print(f"Timeline: {timeline['status']} (Expected: {timeline['expected']} days, Proposed: {timeline['proposed']} days)")
    else:
        print(f"Timeline: {timeline['status']}")
    
    deliverables = results["deliverables"]
    if deliverables["status"] == "Needs Revision" and deliverables["expected"] and deliverables["proposed"]:
        if deliverables["counteroffer"]:
            counteroffer_text = f", Counteroffer: {deliverables['counteroffer']}"
        else:
            counteroffer_text = ""
        print(f"Deliverables: {deliverables['status']} (Expected: {deliverables['expected']}, Proposed: {deliverables['proposed']}{counteroffer_text})")
    elif deliverables["status"] == "Rejected" and deliverables["expected"] and deliverables["proposed"]:
        print(f"Deliverables: {deliverables['status']} (Expected: {deliverables['expected']}, Proposed: {deliverables['proposed']})")
    else:
        print(f"Deliverables: {deliverables['status']}")

def print_detailed_results(results):
    """Print detailed negotiation results"""
    if "error" in results:
        print(f"Error: {results['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"NEGOTIATION RESULTS")
    print(f"{'='*60}")
    print(f"Project: {results['project_name']} (ID: {results['project_id']})")
    print(f"Client ID: {results['client_id']}")
    print(f"Overall Status: {results['overall_status']}")
    print(f"Summary: {results['summary']}")
    
    print(f"\n{'BUDGET':-^60}")
    budget = results['budget']
    print(f"Status: {budget['status']}")
    print(f"Expected: {format_currency(budget['expected'])}")
    print(f"Proposed: {format_currency(budget['proposed'])}")
    if budget['counteroffer']:
        print(f"Counteroffer: {format_currency(budget['counteroffer'])}")
    
    print(f"\n{'TIMELINE':-^60}")
    timeline = results['timeline']
    print(f"Status: {timeline['status']}")
    print(f"Expected: {timeline['expected']} days" if timeline['expected'] else "Expected: Not specified")
    print(f"Proposed: {timeline['proposed']} days" if timeline['proposed'] else "Proposed: Not specified")
    if timeline['counteroffer']:
        print(f"Counteroffer: {timeline['counteroffer']} days")
    
    print(f"\n{'DELIVERABLES':-^60}")
    deliverables = results['deliverables']
    print(f"Status: {deliverables['status']}")
    print(f"Expected: {deliverables['expected']}" if deliverables['expected'] else "Expected: Not specified")
    print(f"Proposed: {deliverables['proposed']}" if deliverables['proposed'] else "Proposed: Not specified")
    if deliverables['counteroffer']:
        print(f"Counteroffer: {deliverables['counteroffer']}")

def list_projects_and_proposals():
    """List all projects and their proposals"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT p.id, p.name, p.expected_budget, p.expected_timeline_days,
                   COUNT(pr.id) as proposal_count
            FROM projects p
            LEFT JOIN proposals pr ON p.id = pr.project_id
            GROUP BY p.id, p.name, p.expected_budget, p.expected_timeline_days
            ORDER BY p.id
        """)
        
        projects = cursor.fetchall()
        
        print("\nAVAILABLE PROJECTS:")
        print("-" * 80)
        for project in projects:
            pid, name, budget, timeline, proposal_count = project
            print(f"ID: {pid} | {name}")
            print(f"  Expected: {format_currency(budget)}, {timeline} days")
            print(f"  Proposals: {proposal_count}")
            
            # Show proposals for this project
            cursor.execute("""
                SELECT pr.client_id, c.name, pr.proposed_budget, pr.proposed_timeline_days
                FROM proposals pr
                LEFT JOIN clients c ON pr.client_id = c.id
                WHERE pr.project_id = ?
                ORDER BY pr.created_date DESC
            """, (pid,))
            
            proposals = cursor.fetchall()
            for proposal in proposals:
                cid, client_name, prop_budget, prop_timeline = proposal
                client_display = client_name if client_name else f"Client ID {cid}"
                print(f"    → {client_display}: {format_currency(prop_budget)}, {prop_timeline} days")
            print()
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        conn.close()

def main():
    """Main CLI function"""
    
    if len(sys.argv) == 1:
        print("Project Negotiation System")
        print("=" * 40)
        print("Available commands:")
        print("  setup                    - Initialize database tables")
        print("  sample                   - Insert sample data")
        print("  list                     - List all projects and proposals")
        print("  negotiate <pid> <cid>    - Run negotiation analysis")
        print("  detailed <pid> <cid>     - Show detailed negotiation results")
        print("\nExamples:")
        print("  python negotiate.py setup")
        print("  python negotiate.py negotiate 1 2")
        print("  python negotiate.py detailed 1 2")
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        setup_database()
    
    elif command == "sample":
        insert_sample_data()
    
    elif command == "list":
        list_projects_and_proposals()
    
    elif command == "negotiate":
        if len(sys.argv) != 4:
            print("Usage: python negotiate.py negotiate <project_id> <client_id>")
            print("Example: python negotiate.py negotiate 1 2")
            sys.exit(1)
        
        try:
            project_id = int(sys.argv[2])
            client_id = int(sys.argv[3])
        except ValueError:
            print("Error: project_id and client_id must be integers")
            sys.exit(1)
        
        print_negotiation_results(project_id, client_id)
    
    elif command == "detailed":
        if len(sys.argv) != 4:
            print("Usage: python negotiate.py detailed <project_id> <client_id>")
            print("Example: python negotiate.py detailed 1 2")
            sys.exit(1)
        
        try:
            project_id = int(sys.argv[2])
            client_id = int(sys.argv[3])
        except ValueError:
            print("Error: project_id and client_id must be integers")
            sys.exit(1)
        
        results = negotiate_project(project_id, client_id)
        print_detailed_results(results)
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see available commands.")
        sys.exit(1)

if __name__ == "__main__":
    main()
