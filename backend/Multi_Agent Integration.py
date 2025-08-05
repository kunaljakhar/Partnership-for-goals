import sqlite3
import os
import json
import sys
from datetime import datetime

class ProjectMatchingAgent:
    def __init__(self, db_path="data.db"):
        self.db_path = db_path
        self.create_database()
    
    def create_database(self):
        if os.path.exists(self.db_path):
            return
        
        conn = sqlite3.connect(self.db_path)
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
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    
    def insert_sample_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            users = [
                ("Alice Johnson", "alice@email.com", "password123", "python, marketing"),
                ("Bob Chen", "bob@email.com", "securepass456", "javascript, design, photography"),
                ("Carol Davis", "carol@email.com", "mypass789", "data analysis, sql, python")
            ]
            
            for user in users:
                cursor.execute('''
                    INSERT OR IGNORE INTO users (name, email, password, skills)
                    VALUES (?, ?, ?, ?)
                ''', user)
            
            projects = [
                ("Personal Blog", "A simple blog website built with modern web technologies", "python, web, blog"),
                ("Data Dashboard", "Interactive dashboard for visualizing sales data", "data analysis, visualization"),
                ("Mobile Game", "Fun puzzle game for smartphones", "mobile, game, design")
            ]
            
            for project in projects:
                cursor.execute('''
                    INSERT OR IGNORE INTO projects (title, description, tags)
                    VALUES (?, ?, ?)
                ''', project)
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()
    
    def match_projects_for_user(self, user_id):
        conn = sqlite3.connect(self.db_path)
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
        
        except sqlite3.Error:
            return []
        finally:
            conn.close()

class NegotiationAgent:
    def __init__(self, db_path="data.db"):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='projects'
            """)
            
            table_exists = cursor.fetchone() is not None
            
            if table_exists:
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
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proposals (
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
            
            conn.commit()
        except sqlite3.Error:
            pass
        finally:
            conn.close()
    
    def insert_negotiation_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM clients")
            if cursor.fetchone()[0] == 0:
                sample_clients = [
                    ("TechCorp Ltd", "contact@techcorp.com"),
                    ("StartupXYZ", "hello@startupxyz.com"),
                    ("BigBusiness Inc", "projects@bigbusiness.com")
                ]
                cursor.executemany("INSERT INTO clients (name, email) VALUES (?, ?)", sample_clients)
            
            cursor.execute("SELECT COUNT(*) FROM proposals")
            if cursor.fetchone()[0] == 0:
                sample_proposals = [
                    (1, 1, 82000, 110, "Website, Mobile app, Admin panel, Payment gateway, SEO optimization"),
                    (1, 2, 70000, 135, "Website, Mobile app, Basic admin panel"),
                    (2, 1, 95000, 160, "iOS app, Android app, Backend API, Admin dashboard")
                ]
                cursor.executemany("""
                    INSERT INTO proposals (project_id, client_id, proposed_budget, proposed_timeline_days, proposed_deliverables)
                    VALUES (?, ?, ?, ?, ?)
                """, sample_proposals)
            
            conn.commit()
        except sqlite3.Error:
            pass
        finally:
            conn.close()
    
    def negotiate_project(self, project_id, client_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT expected_budget, expected_timeline_days, expected_deliverables, title
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
            
            statuses = [budget_status, timeline_status]
            
            if all(status == "Accepted" for status in statuses):
                overall_status = "Accepted"
            elif any(status == "Rejected" for status in statuses):
                overall_status = "Rejected"
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
                }
            }
        
        except sqlite3.Error as e:
            return {"error": f"Database error: {e}"}
        finally:
            conn.close()

class CommunicationAgent:
    def __init__(self):
        self.templates = {
            'inquiry': self._inquiry_template,
            'proposal': self._proposal_template,
            'acceptance': self._acceptance_template,
            'rejection': self._rejection_template
        }
        
        self.tone_keywords = {
            'formal': ['dear', 'sincerely', 'regards', 'respectfully', 'cordially'],
            'informal': ['hey', 'hi', 'thanks', 'cool', 'awesome'],
            'urgent': ['urgent', 'immediate', 'asap', 'rush', 'emergency', 'critical'],
            'polite': ['please', 'thank you', 'appreciate', 'grateful', 'sorry']
        }
    
    def generate_email(self, sender_name, recipient_name, project_title, message_type, **kwargs):
        if message_type not in self.templates:
            return f"Error: Unknown message type '{message_type}'"
        
        template_func = self.templates[message_type]
        return template_func(sender_name, recipient_name, project_title, **kwargs)
    
    def _inquiry_template(self, sender_name, recipient_name, project_title, **kwargs):
        deadline = kwargs.get('deadline', 'to be discussed')
        budget_range = kwargs.get('budget_range', 'flexible')
        
        return f"""Subject: Project Inquiry - {project_title}

Dear {recipient_name},

I hope this email finds you well. I am writing to inquire about the possibility of collaborating on a project titled "{project_title}".

We are seeking a qualified professional to help us with this initiative. The project deadline is {deadline}, and our budget range is {budget_range}.

I would appreciate the opportunity to discuss this project in more detail at your convenience.

Best regards,
{sender_name}"""
    
    def _proposal_template(self, sender_name, recipient_name, project_title, **kwargs):
        proposal_summary = kwargs.get('proposal_summary', 'Please find attached our detailed proposal.')
        timeline = kwargs.get('timeline', '4-6 weeks')
        
        return f"""Subject: Project Proposal Submission - {project_title}

Dear {recipient_name},

Thank you for the opportunity to submit a proposal for "{project_title}".

{proposal_summary}

Our proposed timeline for completion is {timeline}.

Please review the attached proposal and feel free to contact me with any questions.

Best regards,
{sender_name}"""
    
    def _acceptance_template(self, sender_name, recipient_name, project_title, **kwargs):
        start_date = kwargs.get('start_date', 'as soon as possible')
        
        return f"""Subject: Project Acceptance - {project_title}

Dear {recipient_name},

I am delighted to inform you that we have accepted your proposal for "{project_title}".

We would like to start {start_date}.

Thank you for your professional proposal.

Best regards,
{sender_name}"""
    
    def _rejection_template(self, sender_name, recipient_name, project_title, **kwargs):
        reason = kwargs.get('reason', 'budget constraints and timeline requirements')
        
        return f"""Subject: Project Decision - {project_title}

Dear {recipient_name},

Thank you for your interest in "{project_title}".

After careful consideration, we have decided to move forward with a different approach due to {reason}.

Thank you for your time and consideration.

Best regards,
{sender_name}"""
    
    def analyze_tone(self, email_text):
        text_lower = email_text.lower()
        
        tone_scores = {}
        for tone, keywords in self.tone_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            tone_scores[tone] = score
        
        if max(tone_scores.values()) == 0:
            return "neutral"
        
        if tone_scores['urgent'] > 0:
            return "urgent"
        elif tone_scores['formal'] >= tone_scores['polite'] and tone_scores['formal'] >= tone_scores['informal']:
            return "formal"
        elif tone_scores['polite'] >= tone_scores['informal']:
            return "polite"
        else:
            return "informal"

class DocumentationAgent:
    def __init__(self):
        self.org_defaults = {}
        self.project_data = {}
        self.history_file = 'document_history.json'
        self.templates = {
            'service_agreement': """
MEMORANDUM OF UNDERSTANDING - SERVICE AGREEMENT

Between: {organization_name}
And: {client_name}

Project: {project_title}
Description: {project_description}

Timeline: {timeline}
Budget: {budget}

This MOU establishes the framework for service delivery between the parties.

Signed: _________________ Date: _________
{organization_name}

Signed: _________________ Date: _________
{client_name}
""",
            
            'project_collaboration': """
MEMORANDUM OF UNDERSTANDING - PROJECT COLLABORATION

Collaborating Organizations:
- {organization_name}
- {client_name}

Project Title: {project_title}
Project Overview: {project_description}

Project Timeline: {timeline}
Estimated Budget: {budget}

This MOU outlines the collaborative partnership for joint project execution.

For {organization_name}: _________________ Date: _________

For {client_name}: _________________ Date: _________
"""
        }
        
        self.letter_templates = {
            'proposal_acceptance': """
{date}

{client_name}
{client_address}

Subject: Acceptance of Project Proposal - {project_title}

Dear {client_name},

We are pleased to formally accept your project proposal for {project_title}. 

We look forward to a successful collaboration.

Sincerely,

{sender_name}
{sender_title}
{organization_name}
""",
            
            'project_completion': """
{date}

{client_name}
{client_address}

Subject: Project Completion Notification - {project_title}

Dear {client_name},

We are pleased to inform you that {project_title} has been successfully completed.

Thank you for your collaboration throughout this project.

Best regards,

{sender_name}
{sender_title}
{organization_name}
"""
        }
        
        self.required_fields = ['client_name', 'organization_name', 'project_title', 
                               'project_description', 'timeline', 'budget']
    
    def generate_mou(self, template_type, data):
        if template_type not in self.templates:
            raise ValueError(f"Template '{template_type}' not found")
        
        merged_data = self.org_defaults.copy()
        merged_data.update(data)
        
        missing_fields = [field for field in self.required_fields if not merged_data.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        template = self.templates[template_type]
        return template.format(**merged_data).strip()
    
    def generate_letter(self, letter_type, data):
        if letter_type not in self.letter_templates:
            raise ValueError(f"Letter type '{letter_type}' not found")
        
        merged_data = self.org_defaults.copy()
        merged_data.update(data)
        
        if 'date' not in merged_data:
            merged_data['date'] = datetime.now().strftime("%B %d, %Y")
        
        template = self.letter_templates[letter_type]
        return template.format(**merged_data).strip()
    
    def save_document(self, content, doc_type, project_name="document"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{doc_type}_{project_name}_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(content)
            self._log_document(filename, doc_type, project_name)
            return filename
        except Exception as e:
            raise IOError(f"Failed to save document: {e}")
    
    def _log_document(self, filename, doc_type, project_name):
        history = self._load_history()
        history.append({
            'filename': filename,
            'type': doc_type,
            'project': project_name,
            'date': datetime.now().isoformat()
        })
        self._save_history(history)
    
    def _load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_history(self, history):
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

class MultiAgentSystem:
    def __init__(self):
        self.project_agent = ProjectMatchingAgent()
        self.negotiation_agent = NegotiationAgent()
        self.communication_agent = CommunicationAgent()
        self.documentation_agent = DocumentationAgent()
        
        self.project_agent.insert_sample_data()
        self.negotiation_agent.insert_negotiation_data()
    
    def find_project_matches(self, user_id):
        return self.project_agent.match_projects_for_user(user_id)
    
    def negotiate_proposal(self, project_id, client_id):
        return self.negotiation_agent.negotiate_project(project_id, client_id)
    
    def generate_communication(self, sender_name, recipient_name, project_title, message_type, **kwargs):
        return self.communication_agent.generate_email(sender_name, recipient_name, project_title, message_type, **kwargs)
    
    def analyze_email_tone(self, email_text):
        return self.communication_agent.analyze_tone(email_text)
    
    def create_document(self, doc_type, template_type, data):
        if doc_type == 'mou':
            return self.documentation_agent.generate_mou(template_type, data)
        elif doc_type == 'letter':
            return self.documentation_agent.generate_letter(template_type, data)
        else:
            raise ValueError("Document type must be 'mou' or 'letter'")
    
    def save_generated_document(self, content, doc_type, project_name):
        return self.documentation_agent.save_document(content, doc_type, project_name)
    
    def set_organization_defaults(self, **kwargs):
        self.documentation_agent.org_defaults = kwargs
    
    def full_project_workflow(self, user_id, project_id, client_id, sender_name, recipient_name, org_data):
        results = {}
        
        results['matches'] = self.find_project_matches(user_id)
        
        results['negotiation'] = self.negotiate_proposal(project_id, client_id)
        
        if results['negotiation'].get('overall_status') == 'Accepted':
            results['acceptance_email'] = self.generate_communication(
                sender_name, recipient_name, 
                results['negotiation']['project_name'], 
                'acceptance'
            )
        else:
            results['rejection_email'] = self.generate_communication(
                sender_name, recipient_name,
                results['negotiation']['project_name'],
                'rejection'
            )
        
        self.set_organization_defaults(**org_data)
        
        doc_data = {
            'client_name': recipient_name,
            'project_title': results['negotiation']['project_name'],
            'project_description': 'Project collaboration agreement',
            'timeline': str(results['negotiation']['timeline']['expected']) + ' days',
            'budget': 'Rs. ' + str(results['negotiation']['budget']['expected'])
        }
        
        results['mou'] = self.create_document('mou', 'service_agreement', doc_data)
        
        results['saved_mou'] = self.save_generated_document(
            results['mou'], 'mou', 
            results['negotiation']['project_name']
        )
        
        return results

def demo_multiagent_system():
    system = MultiAgentSystem()
    
    org_data = {
        'organization_name': 'TechSolutions Inc',
        'sender_name': 'John Manager',
        'sender_title': 'Project Manager'
    }
    
    print("Multi-Agent System Demo")
    print("=" * 50)
    
    user_id = 1
    project_id = 1
    client_id = 1
    
    results = system.full_project_workflow(
        user_id=user_id,
        project_id=project_id, 
        client_id=client_id,
        sender_name="John Manager",
        recipient_name="TechCorp Ltd",
        org_data=org_data
    )
    
    print("\n1. Project Matches:")
    for i, match in enumerate(results['matches'][:2], 1):
        print(f"   {i}. {match['title']} - Score: {match['match_count']}")
    
    print(f"\n2. Negotiation Status: {results['negotiation']['overall_status']}")
    print(f"   Budget: {results['negotiation']['budget']['status']}")
    print(f"   Timeline: {results['negotiation']['timeline']['status']}")
    
    print("\n3. Generated Email:")
    if 'acceptance_email' in results:
        print(results['acceptance_email'][:200] + "...")
    else:
        print(results['rejection_email'][:200] + "...")
    
    print(f"\n4. Document Created: {results['saved_mou']}")
    
    print("\n5. Email Tone Analysis:")
    sample_email = "Dear Sir, I urgently need this project completed ASAP. Please respond immediately."
    tone = system.analyze_email_tone(sample_email)
    print(f"   Detected tone: {tone}")
    
    return system

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_multiagent_system()
    else:
        system = MultiAgentSystem()
        print("Multi-Agent System initialized successfully!")
        print("Available methods:")
        print("- find_project_matches(user_id)")
        print("- negotiate_proposal(project_id, client_id)")
        print("- generate_communication(sender, recipient, project, type)")
        print("- analyze_email_tone(email_text)")
        print("- create_document(doc_type, template_type, data)")
        print("- full_project_workflow(user_id, project_id, client_id, sender, recipient, org_data)")
        print("\nRun with 'demo' argument to see example usage.")