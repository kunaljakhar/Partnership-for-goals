from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import os
import json
from datetime import datetime
import io
import zipfile

app = Flask(__name__)

class ProjectMatchingAgent:
    def __init__(self):
        self.db_path = "data.db"
        self.create_database()
    
    def create_database(self):
        """Create SQLite database with users and projects tables"""
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
                    tags TEXT,
                    expected_budget INTEGER,
                    expected_timeline_days INTEGER,
                    expected_deliverables TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT
                )
            ''')
            
            cursor.execute('''
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
            ''')
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    
    def add_sample_data(self):
        """Insert sample data if not exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if data already exists
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                users = [
                    ("Alice Johnson", "alice@email.com", "password123", "python, marketing"),
                    ("Bob Chen", "bob@email.com", "securepass456", "javascript, design, photography"),
                    ("Carol Davis", "carol@email.com", "mypass789", "data analysis, sql, python")
                ]
                cursor.executemany('INSERT INTO users (name, email, password, skills) VALUES (?, ?, ?, ?)', users)
            
            cursor.execute("SELECT COUNT(*) FROM projects")
            if cursor.fetchone()[0] == 0:
                projects = [
                    ("Personal Blog", "A simple blog website built with modern web technologies", "python, web, blog", 75000, 120, "Website, Mobile app, Admin panel"),
                    ("Data Dashboard", "Interactive dashboard for visualizing sales data", "data analysis, visualization", 100000, 180, "Dashboard, API, Documentation"),
                    ("Mobile Game", "Fun puzzle game for smartphones", "mobile, game, design", 25000, 45, "Game app, Graphics, Testing")
                ]
                cursor.executemany('INSERT INTO projects (title, description, tags, expected_budget, expected_timeline_days, expected_deliverables) VALUES (?, ?, ?, ?, ?, ?)', projects)
            
            cursor.execute("SELECT COUNT(*) FROM clients")
            if cursor.fetchone()[0] == 0:
                clients = [
                    ("TechCorp Ltd", "contact@techcorp.com"),
                    ("StartupXYZ", "hello@startupxyz.com"),
                    ("BigBusiness Inc", "projects@bigbusiness.com")
                ]
                cursor.executemany('INSERT INTO clients (name, email) VALUES (?, ?)', clients)
            
            cursor.execute("SELECT COUNT(*) FROM proposals")
            if cursor.fetchone()[0] == 0:
                proposals = [
                    (1, 1, 82000, 110, "Website, Mobile app, Admin panel, SEO optimization"),
                    (1, 2, 70000, 135, "Website, Mobile app, Basic admin panel"),
                    (2, 1, 95000, 160, "Dashboard, API, Documentation, Training")
                ]
                cursor.executemany('INSERT INTO proposals (project_id, client_id, proposed_budget, proposed_timeline_days, proposed_deliverables) VALUES (?, ?, ?, ?, ?)', proposals)
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"Error inserting sample data: {e}")
        finally:
            conn.close()
    
    def match_projects_for_user(self, user_id):
        """Find matching projects for a user based on skills"""
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
            
            user_skills_set = set(skill.strip().lower() for skill in user_skills.split(','))
            
            cursor.execute("SELECT id, title, description, tags, expected_budget, expected_timeline_days FROM projects")
            all_projects = cursor.fetchall()
            
            project_matches = []
            for project in all_projects:
                project_id, title, description, tags, budget, timeline = project
                
                if tags:
                    project_tags_set = set(tag.strip().lower() for tag in tags.split(','))
                    matched_skills = user_skills_set.intersection(project_tags_set)
                    match_count = len(matched_skills)
                    
                    if match_count > 0:
                        project_matches.append({
                            'project_id': project_id,
                            'title': title,
                            'description': description,
                            'tags': tags,
                            'expected_budget': budget,
                            'expected_timeline_days': timeline,
                            'match_count': match_count,
                            'matched_skills': list(matched_skills)
                        })
            
            project_matches.sort(key=lambda x: (-x['match_count'], x['title']))
            return project_matches[:3]
        
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    
    def get_all_users(self):
        """Get all users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id, name, email, skills FROM users")
            return cursor.fetchall()
        except sqlite3.Error:
            return []
        finally:
            conn.close()
    
    def get_all_projects(self):
        """Get all projects"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id, title, description, tags, expected_budget, expected_timeline_days FROM projects")
            return cursor.fetchall()
        except sqlite3.Error:
            return []
        finally:
            conn.close()



class NegotiationAgent:
    def __init__(self, db_path="data.db"):
        self.db_path = db_path
    
    def negotiate_project(self, project_id, client_id):
        """Compare project expectations with client proposal"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT expected_budget, expected_timeline_days, expected_deliverables, title
                FROM projects WHERE id = ?
            """, (project_id,))
            
            project_data = cursor.fetchone()
            if not project_data:
                return {"error": f"Project {project_id} not found"}
            
            expected_budget, expected_timeline, expected_deliverables, project_name = project_data
            
            cursor.execute("""
                SELECT proposed_budget, proposed_timeline_days, proposed_deliverables
                FROM proposals WHERE project_id = ? AND client_id = ?
                ORDER BY created_date DESC LIMIT 1
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
            
            deliverables_status = "Accepted" if expected_deliverables == proposed_deliverables else "Needs Revision"
            
            statuses = [budget_status, timeline_status, deliverables_status]
            
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
                },
                "deliverables": {
                    "status": deliverables_status,
                    "expected": expected_deliverables,
                    "proposed": proposed_deliverables
                }
            }
        
        except sqlite3.Error as e:
            return {"error": f"Database error: {e}"}
        finally:
            conn.close()
    
    def get_all_proposals(self):
        """Get all proposals with project and client info"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT p.id, pr.title, c.name, p.proposed_budget, p.proposed_timeline_days, p.client_id
                FROM proposals p
                JOIN projects pr ON p.project_id = pr.id
                JOIN clients c ON p.client_id = c.id
                ORDER BY p.created_date DESC
            """)
            return cursor.fetchall()
        except sqlite3.Error:
            return []
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
        
        self.priority_keywords = {
            'high_urgency': {'urgent': 5, 'emergency': 5, 'critical': 4, 'asap': 4},
            'medium_urgency': {'soon': 2, 'quickly': 2, 'important': 2},
            'project_phases': {'proposal': 3, 'negotiation': 4, 'contract': 4}
        }
    
    def generate_email(self, sender_name, recipient_name, project_title, message_type, **kwargs):
        """Generate email template"""
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
        
        return f"""Subject: Project Proposal - {project_title}

Dear {recipient_name},

Thank you for the opportunity to submit a proposal for "{project_title}".

{proposal_summary}

Our proposed timeline for completion is {timeline}.

Please review the proposal and feel free to contact me with any questions.

Best regards,
{sender_name}"""
    
    def _acceptance_template(self, sender_name, recipient_name, project_title, **kwargs):
        start_date = kwargs.get('start_date', 'as soon as possible')
        
        return f"""Subject: Project Acceptance - {project_title}

Dear {recipient_name},

I am delighted to inform you that we have accepted your proposal for "{project_title}".

We would like to start {start_date}. We will send you a detailed project plan within 48 hours.

Thank you for your professional proposal.

Best regards,
{sender_name}"""
    
    def _rejection_template(self, sender_name, recipient_name, project_title, **kwargs):
        reason = kwargs.get('reason', 'budget constraints')
        
        return f"""Subject: Project Decision - {project_title}

Dear {recipient_name},

Thank you for your proposal for "{project_title}".

After careful consideration, we have decided to move forward with a different approach due to {reason}.

We appreciate your professionalism and would be happy to consider you for future opportunities.

Best regards,
{sender_name}"""
    
    def analyze_tone(self, email_text):
        """Analyze email tone"""
        text_lower = email_text.lower()
        
        tone_scores = {}
        for tone, keywords in self.tone_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            tone_scores[tone] = score
        
        if max(tone_scores.values()) == 0:
            return "neutral"
        
        return max(tone_scores, key=tone_scores.get)
    
    def classify_priority(self, email_content):
        """Classify email priority"""
        text_lower = email_content.lower()
        
        total_score = 0
        matched_keywords = []
        
        for category, keywords in self.priority_keywords.items():
            for keyword, weight in keywords.items():
                if keyword in text_lower:
                    total_score += weight
                    matched_keywords.append(keyword)
        
        if total_score >= 8:
            priority = "high"
        elif total_score >= 4:
            priority = "medium"
        else:
            priority = "low"
        
        return {
            'priority': priority,
            'score': total_score,
            'keywords_found': matched_keywords
        }



class DocumentationAgent:
    def __init__(self):
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
Timeline: {timeline}
Budget: {budget}

This MOU outlines the collaborative partnership for joint project execution.

For {organization_name}: _________________ Date: _________
For {client_name}: _________________ Date: _________
"""
        }
        
        self.letter_templates = {
            'proposal_acceptance': """
{date}

{client_name}

Subject: Acceptance of Project Proposal - {project_title}

Dear {client_name},

We are pleased to accept your project proposal for {project_title}.

Project details:
- Description: {project_description}
- Timeline: {timeline}
- Budget: {budget}

We look forward to a successful collaboration.

Sincerely,
{sender_name}
{organization_name}
""",
            'project_completion': """
{date}

{client_name}

Subject: Project Completion - {project_title}

Dear {client_name},

We are pleased to inform you that {project_title} has been successfully completed.

Thank you for your collaboration throughout this project.

Best regards,
{sender_name}
{organization_name}
"""
        }
    
    def generate_mou(self, template_type, data):
        """Generate MOU document"""
        if template_type not in self.templates:
            raise ValueError(f"Template '{template_type}' not found")
        
        template = self.templates[template_type]
        return template.format(**data).strip()
    
    def generate_letter(self, letter_type, data):
        """Generate letter document"""
        if letter_type not in self.letter_templates:
            raise ValueError(f"Letter type '{letter_type}' not found")
        
        if 'date' not in data:
            data['date'] = datetime.now().strftime("%B %d, %Y")
        
        template = self.letter_templates[letter_type]
        return template.format(**data).strip()



class MultiAgentSystem:
    def __init__(self):
        self.project_agent = ProjectMatchingAgent()
        self.negotiation_agent = NegotiationAgent()
        self.communication_agent = CommunicationAgent()
        self.documentation_agent = DocumentationAgent()
        
        # Initialize with sample data
        self.project_agent.add_sample_data()
    
    def get_dashboard_data(self):
        """Get dashboard statistics"""
        users = self.project_agent.get_all_users()
        projects = self.project_agent.get_all_projects()
        proposals = self.negotiation_agent.get_all_proposals()
        
        return {
            'total_users': len(users),
            'total_projects': len(projects),
            'total_proposals': len(proposals),
            'users': users[:5],  # Recent 5
            'projects': projects[:5],  # Recent 5
            'proposals': proposals[:5]  # Recent 5
        }



# Initialize the multi-agent system
mas = MultiAgentSystem()

@app.route('/')
def dashboard():
    """Main dashboard"""
    data = mas.get_dashboard_data()
    return render_template('dashboard.html', **data)

@app.route('/project-matching')
def project_matching():
    """Project matching interface"""
    users = mas.project_agent.get_all_users()
    return render_template('project_matching.html', users=users)

@app.route('/api/match-projects/<int:user_id>')
def api_match_projects(user_id):
    """API endpoint for project matching"""
    matches = mas.project_agent.match_projects_for_user(user_id)
    return jsonify(matches)

@app.route('/negotiation')
def negotiation():
    """Negotiation interface"""
    projects = mas.project_agent.get_all_projects()
    proposals = mas.negotiation_agent.get_all_proposals()
    return render_template('negotiation.html', projects=projects, proposals=proposals)

@app.route('/api/negotiate/<int:project_id>/<int:client_id>')
def api_negotiate(project_id, client_id):
    """API endpoint for negotiation"""
    result = mas.negotiation_agent.negotiate_project(project_id, client_id)
    return jsonify(result)

@app.route('/communication')
def communication():
    """Communication interface"""
    return render_template('communication.html')

@app.route('/api/generate-email', methods=['POST'])
def api_generate_email():
    """API endpoint for email generation"""
    data = request.json
    try:
        email = mas.communication_agent.generate_email(
            data['sender_name'],
            data['recipient_name'],
            data['project_title'],
            data['message_type'],
            **data.get('additional_data', {})
        )
        return jsonify({'success': True, 'email': email})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/analyze-email', methods=['POST'])
def api_analyze_email():
    """API endpoint for email analysis"""
    data = request.json
    email_content = data.get('email_content', '')
    
    tone = mas.communication_agent.analyze_tone(email_content)
    priority = mas.communication_agent.classify_priority(email_content)
    
    return jsonify({
        'tone': tone,
        'priority': priority
    })

@app.route('/documentation')
def documentation():
    """Documentation interface"""
    return render_template('documentation.html')

@app.route('/api/generate-document', methods=['POST'])
def api_generate_document():
    """API endpoint for document generation"""
    data = request.json
    doc_type = data['doc_type']
    template_type = data['template_type']
    doc_data = data['doc_data']
    
    try:
        if doc_type == 'mou':
            document = mas.documentation_agent.generate_mou(template_type, doc_data)
        else:
            document = mas.documentation_agent.generate_letter(template_type, doc_data)
        
        return jsonify({'success': True, 'document': document})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/download-document', methods=['POST'])
def api_download_document():
    """API endpoint for document download"""
    data = request.json
    content = data['content']
    filename = data.get('filename', 'document.txt')
    
    # Create a file-like object
    file_obj = io.StringIO(content)
    file_obj.seek(0)
    
    return send_file(
        io.BytesIO(content.encode('utf-8')),
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))