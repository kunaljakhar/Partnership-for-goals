from datetime import datetime
import os
import json

class DocumentationAgent:
    def __init__(self):
        self.org_defaults = {}
        self.project_data = {}
        self.history_file = 'document_history.json'
        self.config_file = 'config.json'
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
Both parties agree to collaborate professionally to achieve project objectives.

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
Resources and responsibilities will be shared as mutually agreed upon.

For {organization_name}: _________________ Date: _________

For {client_name}: _________________ Date: _________
""",
            
            'consulting': """
MEMORANDUM OF UNDERSTANDING - CONSULTING SERVICES

Consultant: {organization_name}
Client: {client_name}

Consulting Engagement: {project_title}
Scope of Work: {project_description}

Duration: {timeline}
Fee Structure: {budget}

This MOU defines the consulting relationship and service expectations.
Deliverables and milestones will be detailed in subsequent agreements.

Consultant Signature: _________________ Date: _________

Client Signature: _________________ Date: _________
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
After careful review, we confirm our commitment to deliver {project_description} 
within the agreed timeline of {timeline}.

The project will commence on {start_date} with an estimated budget of {budget}. 
We look forward to a successful collaboration and will provide regular updates 
throughout the project lifecycle.

Please find the signed agreement attached for your records.

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

We are pleased to inform you that {project_title} has been successfully completed 
as of {completion_date}. All deliverables outlined in our agreement have been 
delivered according to specifications.

Project Summary:
- {project_description}
- Timeline: {timeline}
- Final Budget: {budget}

Thank you for your collaboration throughout this project. We hope you are 
satisfied with the results and look forward to future opportunities.

Best regards,

{sender_name}
{sender_title}
{organization_name}
""",
            
            'payment_request': """
{date}

{client_name}
{client_address}

Subject: Payment Request - Invoice #{invoice_number}

Dear {client_name},

This letter serves as a formal request for payment regarding {project_title}. 
The services have been completed as agreed, and payment is now due.

Invoice Details:
- Project: {project_description}
- Amount Due: {budget}
- Due Date: {due_date}

Please remit payment within 30 days of receipt. If you have any questions 
regarding this invoice, please contact us immediately.

Thank you for your prompt attention to this matter.

Sincerely,

{sender_name}
{sender_title}
{organization_name}
""",
            
            'project_summary': """
{date}

PROJECT SUMMARY REPORT

Project: {project_title}
Client: {client_name}
Duration: {timeline}
Budget: {budget}

OVERVIEW:
{project_description}

STATUS: {project_status}

DELIVERABLES:
{deliverables}

NEXT STEPS:
{next_steps}

Prepared by: {sender_name}
{organization_name}
"""
        }
        
        self.required_fields = ['client_name', 'organization_name', 'project_title', 
                               'project_description', 'timeline', 'budget']
        self.letter_required_fields = ['client_name', 'client_address', 'sender_name', 
                                      'sender_title', 'organization_name', 'project_title']
        self.load_templates_from_config()
    
    def load_templates_from_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                if 'mou_templates' in config:
                    self.templates.update(config['mou_templates'])
                if 'letter_templates' in config:
                    self.letter_templates.update(config['letter_templates'])
        except FileNotFoundError:
            self._create_default_config()
    
    def add_new_template(self, template_name, template_content, template_type='mou'):
        if template_type == 'mou':
            self.templates[template_name] = template_content
        else:
            self.letter_templates[template_name] = template_content
        self._save_templates_to_config()
        return f"Template '{template_name}' added successfully"
    
    def list_available_templates(self):
        return {
            'mou_templates': list(self.templates.keys()),
            'letter_templates': list(self.letter_templates.keys())
        }
    
    def _create_default_config(self):
        config = {
            'mou_templates': self.templates,
            'letter_templates': self.letter_templates
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _save_templates_to_config(self):
        config = {
            'mou_templates': self.templates,
            'letter_templates': self.letter_templates
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_project_data(self, project_dict):
        self.project_data = project_dict.copy()
        required_project_fields = ['name', 'description', 'client_info', 'timeline', 'budget']
        missing_fields = [field for field in required_project_fields if field not in project_dict]
        if missing_fields:
            raise ValueError(f"Missing required project fields: {missing_fields}")
        return "Project data loaded successfully"
    
    def _auto_populate_fields(self, data, client_data=None):
        populated_data = data.copy()
        if self.project_data:
            populated_data.setdefault('project_title', self.project_data.get('name', ''))
            populated_data.setdefault('project_description', self.project_data.get('description', ''))
            populated_data.setdefault('timeline', self.project_data.get('timeline', ''))
            populated_data.setdefault('budget', self.project_data.get('budget', ''))
            populated_data.setdefault('project_status', self.project_data.get('status', 'Active'))
            populated_data.setdefault('deliverables', self.project_data.get('deliverables', 'As specified in agreement'))
            populated_data.setdefault('next_steps', self.project_data.get('next_steps', 'Continue as planned'))
        if client_data:
            populated_data.setdefault('client_name', client_data.get('name', ''))
            populated_data.setdefault('client_address', client_data.get('address', ''))
        elif self.project_data and 'client_info' in self.project_data:
            client_info = self.project_data['client_info']
            populated_data.setdefault('client_name', client_info.get('name', ''))
            populated_data.setdefault('client_address', client_info.get('address', ''))
        return populated_data
    
    def generate_mou(self, template_type, data, client_data=None):
        if template_type not in self.templates:
            raise ValueError(f"Template '{template_type}' not found. Available: {list(self.templates.keys())}")
        populated_data = self._auto_populate_fields(data, client_data)
        merged_data = self._merge_defaults(populated_data)
        missing_fields = [field for field in self.required_fields if not merged_data.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        template = self.templates[template_type]
        return self._apply_formatting(template.format(**merged_data).strip())
    
    def generate_letter(self, letter_type, data, client_data=None):
        if letter_type not in self.letter_templates:
            raise ValueError(f"Letter type '{letter_type}' not found. Available: {list(self.letter_templates.keys())}")
        populated_data = self._auto_populate_fields(data, client_data)
        merged_data = self._merge_defaults(populated_data)
        if 'date' not in merged_data:
            merged_data['date'] = datetime.now().strftime("%B %d, %Y")
        template = self.letter_templates[letter_type]
        return self._apply_formatting(template.format(**merged_data).strip())
    
    def generate_complete_package(self, mou_type='service_agreement', additional_data=None, client_data=None):
        if not self.project_data:
            raise ValueError("Project data must be loaded before generating complete package")
        data = additional_data or {}
        results = {}
        try:
            results['mou'] = self.generate_mou(mou_type, data, client_data)
            results['cover_letter'] = self.generate_letter('proposal_acceptance', data, client_data)
            results['project_summary'] = self.generate_letter('project_summary', data, client_data)
            return results
        except Exception as e:
            raise ValueError(f"Failed to generate complete package: {e}")
    
    def save_document(self, content, doc_type, project_name="document"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{doc_type}_{project_name}_{timestamp}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(content)
            self._log_document(filename, doc_type, project_name, content)
            return filename
        except Exception as e:
            raise IOError(f"Failed to save document: {e}")
    
    def list_generated_documents(self):
        try:
            files = [f for f in os.listdir('.') if f.endswith('.txt') and 
                    any(doc_type in f for doc_type in ['mou', 'letter', 'service_agreement', 
                                                      'project_collaboration', 'consulting',
                                                      'proposal_acceptance', 'project_completion', 
                                                      'payment_request'])]
            return sorted(files, reverse=True)
        except Exception as e:
            raise IOError(f"Failed to list documents: {e}")
    
    def set_organization_defaults(self, **kwargs):
        self.org_defaults = kwargs
    
    def customize_template(self, template_type, section, new_content):
        if template_type in self.templates:
            self.templates[template_type] = self.templates[template_type].replace(section, new_content)
        elif template_type in self.letter_templates:
            self.letter_templates[template_type] = self.letter_templates[template_type].replace(section, new_content)
    
    def _apply_formatting(self, text):
        text = text.replace('', '').replace('*bold', '*BOLD*')
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip().startswith('* '):
                formatted_lines.append('  • ' + line.strip()[2:])
            else:
                formatted_lines.append(line)
        return '\n'.join(formatted_lines)
    
    def _merge_defaults(self, data):
        merged_data = self.org_defaults.copy()
        merged_data.update(data)
        return merged_data
    
    def preview_document(self, doc_type, template_type, data, client_data=None):
        populated_data = self._auto_populate_fields(data, client_data)
        merged_data = self._merge_defaults(populated_data)
        if doc_type == 'mou':
            content = self.generate_mou(template_type, merged_data, client_data)
        else:
            content = self.generate_letter(template_type, merged_data, client_data)
        return self._apply_formatting(content)
    
    def _log_document(self, filename, doc_type, project_name, content):
        history = self._load_history()
        client_name = self._extract_client_name(content)
        history.append({
            'filename': filename,
            'type': doc_type,
            'project': project_name,
            'client': client_name,
            'date': datetime.now().isoformat(),
            'title': f"{doc_type.replace('_', ' ').title()} - {project_name}"
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
    
    def _extract_client_name(self, content):
        lines = content.split('\n')
        for line in lines:
            if 'Client:' in line or 'And:' in line:
                return line.split(':')[-1].strip()
        return "Unknown"
    
    def search_documents(self, query):
        history = self._load_history()
        results = []
        query_lower = query.lower()
        for doc in history:
            if (query_lower in doc['project'].lower() or 
                query_lower in doc['client'].lower() or 
                query_lower in doc['title'].lower()):
                results.append(doc)
        return results
    
    def update_document(self, filename, new_content):
        try:
            with open(filename, 'w') as f:
                f.write(new_content)
            return f"Document {filename} updated successfully"
        except Exception as e:
            raise IOError(f"Failed to update document: {e}")
    
    def get_document_stats(self):
        history = self._load_history()
        stats = {}
        for doc in history:
            doc_type = doc['type']
            stats[doc_type] = stats.get(doc_type, 0) + 1
        return stats
