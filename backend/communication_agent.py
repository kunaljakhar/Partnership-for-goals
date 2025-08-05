class CommunicationAgent:
    """Simple email template generator for project collaboration with tone analysis."""
    
    def _init_(self):
        self.templates = {
            'inquiry': self._inquiry_template,
            'proposal': self._proposal_template,
            'acceptance': self._acceptance_template,
            'rejection': self._rejection_template
        }
        
        # Tone analysis keywords
        self.tone_keywords = {
            'formal': ['dear', 'sincerely', 'regards', 'respectfully', 'cordially', 'hereby', 
                      'furthermore', 'therefore', 'accordingly', 'pursuant', 'kindly'],
            'informal': ['hey', 'hi', 'thanks', 'cool', 'awesome', 'sure thing', 'no problem',
                        'catch up', 'touch base', 'heads up', 'fyi', 'btw', 'asap'],
            'urgent': ['urgent', 'immediate', 'asap', 'rush', 'emergency', 'critical', 
                      'deadline', 'time-sensitive', 'priority', 'quickly', 'immediately'],
            'polite': ['please', 'thank you', 'appreciate', 'grateful', 'sorry', 'excuse me',
                      'would you mind', 'if possible', 'at your convenience', 'kindly', 'gracious']
        }
        
        # Response suggestion keywords
        self.response_keywords = {
            'project_questions': ['question', 'clarify', 'unclear', 'explain', 'details', 
                                'understand', 'confused', 'help', 'what', 'how', 'when', 'where'],
            'deadline_discussions': ['deadline', 'timeline', 'schedule', 'delivery', 'completion',
                                   'due date', 'extend', 'delay', 'rush', 'sooner', 'later'],
            'payment_terms': ['payment', 'invoice', 'cost', 'price', 'budget', 'fee', 'billing',
                            'deposit', 'installment', 'refund', 'expense', 'rate', 'quote'],
            'project_updates': ['update', 'progress', 'status', 'milestone', 'completed', 
                              'finished', 'working on', 'next phase', 'report', 'summary']
        }
        
        # Priority classification keywords with weights
        self.priority_keywords = {
            'high_urgency': {'urgent': 5, 'emergency': 5, 'critical': 4, 'asap': 4, 'immediate': 4,
                           'immediately': 4, 'rush': 3, 'priority': 3, 'deadline': 3},
            'medium_urgency': {'soon': 2, 'quickly': 2, 'important': 2, 'needed': 2, 
                             'required': 2, 'time-sensitive': 3},
            'project_phases': {'proposal': 3, 'negotiation': 4, 'contract': 4, 'execution': 2,
                             'completion': 4, 'delivery': 3, 'final': 3, 'launch': 4}
        }
    
    def generate_email(self, sender_name, recipient_name, project_title, message_type, **kwargs):
        """
        Generate a formal email template.
        
        Args:
            sender_name (str): Name of the email sender
            recipient_name (str): Name of the email recipient
            project_title (str): Title of the project
            message_type (str): Type of email (inquiry, proposal, acceptance, rejection)
            **kwargs: Additional parameters specific to each template
        
        Returns:
            str: Formatted email template
        """
        if message_type not in self.templates:
            return f"Error: Unknown message type '{message_type}'. Available types: {list(self.templates.keys())}"
        
        template_func = self.templates[message_type]
        return template_func(sender_name, recipient_name, project_title, **kwargs)
    
    def _inquiry_template(self, sender_name, recipient_name, project_title, **kwargs):
        """Template for project inquiry emails."""
        deadline = kwargs.get('deadline', 'to be discussed')
        budget_range = kwargs.get('budget_range', 'flexible')
        
        return f"""Subject: Project Inquiry - {project_title}

Dear {recipient_name},

I hope this email finds you well. I am writing to inquire about the possibility of collaborating on a project titled "{project_title}".

We are seeking a qualified professional to help us with this initiative. The project deadline is {deadline}, and our budget range is {budget_range}.

I would appreciate the opportunity to discuss this project in more detail at your convenience. Please let me know if you are interested and available for a brief conversation.

Thank you for your time and consideration.

Best regards,
{sender_name}"""
    
    def _proposal_template(self, sender_name, recipient_name, project_title, **kwargs):
        """Template for project proposal submission emails."""
        proposal_summary = kwargs.get('proposal_summary', 'Please find attached our detailed proposal.')
        timeline = kwargs.get('timeline', '4-6 weeks')
        
        return f"""Subject: Project Proposal Submission - {project_title}

Dear {recipient_name},

Thank you for the opportunity to submit a proposal for "{project_title}". We are excited about the prospect of working with you on this project.

{proposal_summary}

Our proposed timeline for completion is {timeline}. We believe our approach will deliver exceptional results that meet your project objectives.

Please review the attached proposal and feel free to contact me with any questions or clarifications you may need.

We look forward to your feedback and the opportunity to move forward with this collaboration.

Best regards,
{sender_name}"""
    
    def _acceptance_template(self, sender_name, recipient_name, project_title, **kwargs):
        """Template for project acceptance emails."""
        start_date = kwargs.get('start_date', 'as soon as possible')
        next_steps = kwargs.get('next_steps', 'We will send you a detailed project plan within 48 hours.')
        
        return f"""Subject: Project Acceptance - {project_title}

Dear {recipient_name},

I am delighted to inform you that we have accepted your proposal for "{project_title}". After careful review, we believe your approach aligns perfectly with our project goals.

We are excited to begin this collaboration and would like to start {start_date}. {next_steps}

Please confirm your availability and let us know if you need any additional information or resources to get started.

Thank you for your professional proposal, and we look forward to a successful partnership.

Best regards,
{sender_name}"""
    
    def _rejection_template(self, sender_name, recipient_name, project_title, **kwargs):
        """Template for project rejection emails."""
        reason = kwargs.get('reason', 'budget constraints and timeline requirements')
        future_consideration = kwargs.get('future_consideration', True)
        
        rejection_text = f"""Subject: Project Decision - {project_title}

Dear {recipient_name},

Thank you for your interest and the time you invested in submitting a proposal for "{project_title}".

After careful consideration, we have decided to move forward with a different approach due to {reason}. This was a difficult decision as we received several high-quality proposals.

We truly appreciate your professionalism and the quality of your submission."""
        
        if future_consideration:
            rejection_text += f"""

We would be happy to keep your information on file for future opportunities that may be a better fit.

Thank you again for your interest in working with us.

Best regards,
{sender_name}"""
        else:
            rejection_text += f"""

Thank you again for your time and consideration.

Best regards,
{sender_name}"""
        
        return rejection_text
    
    def analyze_tone(self, email_text):
        """
        Analyze the tone of an email using keyword matching.
        
        Args:
            email_text (str): The email content to analyze
            
        Returns:
            str: Detected tone category (formal, informal, urgent, polite)
        """
        # Convert to lowercase for case-insensitive matching
        text_lower = email_text.lower()
        
        # Count matches for each tone category
        tone_scores = {}
        for tone, keywords in self.tone_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            tone_scores[tone] = score
        
        # Determine primary tone based on highest score
        if max(tone_scores.values()) == 0:
            return "neutral"
        
        # Handle ties by priority: urgent > formal > polite > informal
        if tone_scores['urgent'] > 0:
            return "urgent"
        elif tone_scores['formal'] >= tone_scores['polite'] and tone_scores['formal'] >= tone_scores['informal']:
            return "formal"
        elif tone_scores['polite'] >= tone_scores['informal']:
            return "polite"
        else:
            return "informal"
    
    def suggest_responses(self, email_content):
        """
        Suggest appropriate response templates based on email content.
        
        Args:
            email_content (str): The incoming email content to analyze
            
        Returns:
            list: List of 2-3 suggested response types with templates
        """
        text_lower = email_content.lower()
        
        # Count matches for each response category
        category_scores = {}
        for category, keywords in self.response_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            category_scores[category] = score
        
        # Get top scoring categories
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        suggestions = []
        
        # Generate suggestions for top 2-3 categories with matches
        for category, score in sorted_categories[:3]:
            if score > 0:  # Only suggest if keywords were found
                template = self._get_response_template(category)
                suggestions.append({
                    'type': category,
                    'score': score,
                    'template': template
                })
        
        # If no specific matches, suggest general acknowledgment
        if not suggestions:
            suggestions.append({
                'type': 'general_acknowledgment',
                'score': 0,
                'template': self._get_response_template('general_acknowledgment')
            })
        
        return suggestions
    
    def _get_response_template(self, response_type):
        """Generate response template based on type."""
        templates = {
            'project_questions': """Thank you for your questions about the project. I'd be happy to provide clarification.

Let me address your concerns in detail:
[Insert specific answers here]

Please don't hesitate to reach out if you need any additional information.""",
            
            'deadline_discussions': """I understand you'd like to discuss the project timeline.

Based on the current scope, here's what I can offer:
[Insert timeline details here]

I'm open to discussing adjustments if needed to meet your requirements.""",
            
            'payment_terms': """Thank you for bringing up the payment terms. Let me clarify the details:

[Insert payment information here]

I'm happy to discuss alternative arrangements if these terms don't work for your situation.""",
            
            'project_updates': """Thank you for requesting a project update. Here's the current status:

Progress Summary:
[Insert progress details here]

Next Steps:
[Insert upcoming milestones here]

I'll continue to keep you informed as we move forward.""",
            
            'general_acknowledgment': """Thank you for your email. I've received your message and will review it carefully.

I'll get back to you within 24 hours with a detailed response.

Please let me know if you have any urgent concerns in the meantime."""
        }
        
        return templates.get(response_type, templates['general_acknowledgment'])
    
    def classify_priority(self, email_content):
        """
        Classify email priority based on urgency keywords and project phases.
        
        Args:
            email_content (str): The email content to analyze
            
        Returns:
            dict: Priority classification with level and reason
        """
        text_lower = email_content.lower()
        
        # Calculate weighted scores for different categories
        high_urgency_score = 0
        medium_urgency_score = 0
        project_phase_score = 0
        
        matched_keywords = []
        
        # Score high urgency keywords
        for keyword, weight in self.priority_keywords['high_urgency'].items():
            if keyword in text_lower:
                high_urgency_score += weight
                matched_keywords.append(keyword)
        
        # Score medium urgency keywords  
        for keyword, weight in self.priority_keywords['medium_urgency'].items():
            if keyword in text_lower:
                medium_urgency_score += weight
                matched_keywords.append(keyword)
        
        # Score project phase keywords
        for keyword, weight in self.priority_keywords['project_phases'].items():
            if keyword in text_lower:
                project_phase_score += weight
                matched_keywords.append(keyword)
        
        # Calculate total score
        total_score = high_urgency_score + medium_urgency_score + project_phase_score
        
        # Determine priority level and reason
        if high_urgency_score >= 4 or total_score >= 8:
            priority = "high"
            reason = self._get_priority_reason("high", matched_keywords, high_urgency_score, project_phase_score)
        elif medium_urgency_score >= 3 or total_score >= 4 or project_phase_score >= 3:
            priority = "medium" 
            reason = self._get_priority_reason("medium", matched_keywords, medium_urgency_score, project_phase_score)
        else:
            priority = "low"
            reason = "No urgent keywords or critical project phases detected"
        
        return {
            'priority': priority,
            'reason': reason,
            'score': total_score,
            'keywords_found': matched_keywords
        }
    
    def _get_priority_reason(self, priority_level, keywords, urgency_score, phase_score):
        """Generate explanation for priority classification."""
        reasons = []
        
        if urgency_score > 0:
            urgent_words = [kw for kw in keywords if kw in ['urgent', 'emergency', 'critical', 'asap', 'immediate']]
            if urgent_words:
                reasons.append(f"Contains urgent keywords: {', '.join(urgent_words[:2])}")
        
        if phase_score > 0:
            phase_words = [kw for kw in keywords if kw in ['proposal', 'negotiation', 'contract', 'completion', 'delivery', 'launch']]
            if phase_words:
                reasons.append(f"Critical project phase: {', '.join(phase_words[:2])}")
        
        if not reasons:
            if priority_level == "medium":
                reasons.append("Contains time-sensitive or important keywords")
            else:
                reasons.append("Multiple priority indicators detected")
        
        return "; ".join(reasons)
    
    def generate_auto_reply(self, sender_status, email_priority, project_phase=None):
        """
        Generate automatic acknowledgment email with estimated response time.
        
        Args:
            sender_status (str): Sender availability - 'available', 'busy', or 'away'
            email_priority (str): Email priority - 'high', 'medium', or 'low'
            project_phase (str, optional): Current project phase for context
            
        Returns:
            dict: Auto-reply email with subject and body
        """
        # Calculate estimated response time
        response_time = self._calculate_response_time(sender_status, email_priority)
        
        # Generate appropriate subject line
        subject = self._generate_auto_reply_subject(email_priority, sender_status)
        
        # Create email body
        body = self._generate_auto_reply_body(sender_status, email_priority, response_time, project_phase)
        
        return {
            'subject': subject,
            'body': body,
            'estimated_response': response_time,
            'priority_level': email_priority,
            'sender_status': sender_status
        }
    
    def _calculate_response_time(self, status, priority):
        """Calculate estimated response time based on status and priority."""
        base_times = {
            'available': {'high': '2-4 hours', 'medium': '4-8 hours', 'low': '1-2 business days'},
            'busy': {'high': '4-6 hours', 'medium': '8-12 hours', 'low': '2-3 business days'},
            'away': {'high': '12-24 hours', 'medium': '1-2 business days', 'low': '3-5 business days'}
        }
        
        return base_times.get(status, base_times['available']).get(priority, '1-2 business days')
    
    def _generate_auto_reply_subject(self, priority, status):
        """Generate appropriate subject line for auto-reply."""
        if priority == 'high':
            return "Auto-Reply: Message Received - High Priority"
        elif status == 'away':
            return "Auto-Reply: Currently Away - Will Respond Soon"
        else:
            return "Auto-Reply: Message Received - Thank You"
    
    def _generate_auto_reply_body(self, status, priority, response_time, project_phase):
        """Generate the main body of the auto-reply email."""
        # Opening acknowledgment
        opening = "Thank you for your email. This is an automated acknowledgment to confirm that your message has been received."
        
        # Status-specific message
        status_msg = self._get_status_message(status)
        
        # Priority-specific response
        priority_msg = self._get_priority_message(priority, response_time)
        
        # Project phase context (if provided)
        phase_msg = self._get_phase_message(project_phase) if project_phase else ""
        
        # Closing and contact info
        closing = self._get_auto_reply_closing(priority)
        
        # Combine all parts
        body_parts = [opening, status_msg, priority_msg]
        if phase_msg:
            body_parts.append(phase_msg)
        body_parts.append(closing)
        
        return "\n\n".join(filter(None, body_parts))
    
    def _get_status_message(self, status):
        """Get message based on sender's availability status."""
        messages = {
            'available': "I am currently available and actively monitoring emails.",
            'busy': "I am currently in meetings or focused on urgent tasks, but will review your message as soon as possible.",
            'away': "I am currently away from the office but will respond to your message upon my return."
        }
        return messages.get(status, messages['available'])
    
    def _get_priority_message(self, priority, response_time):
        """Get message based on email priority level."""
        if priority == 'high':
            return f"Your message has been marked as HIGH PRIORITY and will be addressed within {response_time}."
        elif priority == 'medium':
            return f"Your message is important and you can expect a detailed response within {response_time}."
        else:
            return f"I will provide a comprehensive response within {response_time}."
    
    def _get_phase_message(self, project_phase):
        """Get context message based on project phase."""
        phase_messages = {
            'proposal': "I understand this relates to the proposal phase. I'll prioritize reviewing proposal-related items.",
            'negotiation': "As we're in the negotiation phase, I'll ensure prompt attention to contract-related matters.",
            'execution': "During the execution phase, I'm monitoring project progress closely and will respond accordingly.",
            'completion': "As we approach project completion, I'll address any final deliverable questions promptly."
        }
        return phase_messages.get(project_phase, "")
    
    def _get_auto_reply_closing(self, priority):
        """Get appropriate closing based on priority."""
        if priority == 'high':
            return """If this is an emergency requiring immediate attention, please call [phone number] or contact [emergency contact].

Best regards,
[Your Name]
[Your Title]
[Contact Information]"""
        else:
            return """If you need immediate assistance, please don't hesitate to call [phone number].

Best regards,
[Your Name]
[Your Title]
[Contact Information]"""


# Example usage
if _name_ == "_main_":
    # Create communication agent
    agent = CommunicationAgent()
    
    # Example 1: Project inquiry
    inquiry_email = agent.generate_email(
        sender_name="Sarah Johnson",
        recipient_name="Mike Chen",
        project_title="Website Redesign Project",
        message_type="inquiry",
        deadline="end of March",
        budget_range="$5,000 - $8,000"
    )
    print("=== PROJECT INQUIRY ===")
    print(inquiry_email)
    print("\n" + "="*50 + "\n")
    
    # Example 2: Proposal submission
    proposal_email = agent.generate_email(
        sender_name="Mike Chen",
        recipient_name="Sarah Johnson", 
        project_title="Website Redesign Project",
        message_type="proposal",
        proposal_summary="Our proposal includes a modern responsive design, SEO optimization, and content management system integration.",
        timeline="6-8 weeks"
    )
    print("=== PROPOSAL SUBMISSION ===")
    print(proposal_email)
    print("\n" + "="*50 + "\n")
    
    # Example 3: Project acceptance
    acceptance_email = agent.generate_email(
        sender_name="Sarah Johnson",
        recipient_name="Mike Chen",
        project_title="Website Redesign Project", 
        message_type="acceptance",
        start_date="next Monday",
        next_steps="Our project manager will contact you tomorrow to schedule a kickoff meeting."
    )
    print("=== PROJECT ACCEPTANCE ===")
    print(acceptance_email)
    print("\n" + "="*50 + "\n")
    
    # Example 4: Tone analysis
    print("=== TONE ANALYSIS ===")
    
    # Test different tones
    urgent_email = "URGENT: Need your proposal ASAP! Deadline is tomorrow, this is critical!"
    formal_email = "Dear Sir/Madam, I hereby respectfully request your kind consideration. Sincerely yours."
    informal_email = "Hey there! Thanks for the awesome work. Let's catch up soon - no problem!"
    polite_email = "Please let me know if this works. Thank you so much, I really appreciate your help."
    
    test_emails = [
        ("Urgent", urgent_email),
        ("Formal", formal_email), 
        ("Informal", informal_email),
        ("Polite", polite_email),
        ("Generated Inquiry", inquiry_email)
    ]
    
    for label, email in test_emails:
        detected_tone = agent.analyze_tone(email)
        print(f"{label} email tone: {detected_tone}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 5: Response suggestions
    print("=== RESPONSE SUGGESTIONS ===")
    
    # Test different incoming email scenarios
    test_scenarios = [
        ("Project Questions", "Hi, I have some questions about the project scope. Can you clarify what deliverables are included? I'm a bit confused about the timeline."),
        ("Deadline Discussion", "We need to discuss the project deadline. Can we extend it by two weeks? The current timeline seems too rushed."),
        ("Payment Inquiry", "I wanted to ask about the payment terms. When is the deposit due? What are your rates for additional work?"),
        ("Status Update Request", "Could you provide an update on the project progress? What milestones have been completed so far?"),
        ("Mixed Content", "Quick question about payment and deadline - can we extend the timeline and adjust the budget accordingly?")
    ]
    
    for scenario_name, email_content in test_scenarios:
        print(f"\n--- {scenario_name} ---")
        print(f"Incoming: {email_content[:60]}...")
        
        suggestions = agent.suggest_responses(email_content)
        print(f"Suggested responses ({len(suggestions)}):")
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion['type'].replace('_', ' ').title()} (score: {suggestion['score']})")
            print(f"   Template preview: {suggestion['template'][:80]}...")
    
    print("\n" + "="*50 + "\n")
    
    # Example 6: Priority classification
    print("=== PRIORITY CLASSIFICATION ===")
    
    priority_test_emails = [
        ("Emergency Bug", "URGENT: Critical bug in production! Need immediate fix ASAP - emergency situation!"),
        ("Contract Negotiation", "We're in the final negotiation phase for the contract. This is important for project completion."),
        ("Regular Update", "Here's the weekly project update. Everything is progressing normally."),
        ("Proposal Deadline", "Quick reminder - the proposal deadline is approaching. Please prioritize this."),
        ("Delivery Phase", "We're entering the final delivery phase. Launch is scheduled for next week."),
        ("Casual Question", "Hi, just wondering about the project status when you have a moment.")
    ]
    
    for email_type, content in priority_test_emails:
        result = agent.classify_priority(content)
        print(f"\n--- {email_type} ---")
        print(f"Content: {content[:60]}...")
        print(f"Priority: {result['priority'].upper()} (score: {result['score']})")
        print(f"Reason: {result['reason']}")
        if result['keywords_found']:
            print(f"Keywords: {result['keywords_found']}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 7: Auto-reply generation
    print("=== AUTO-REPLY GENERATION ===")
    
    auto_reply_scenarios = [
        ("Available + High Priority", "available", "high", "negotiation"),
        ("Busy + Medium Priority", "busy", "medium", "execution"),
        ("Away + Low Priority", "away", "low", None),
        ("Available + Low Priority", "available", "low", "completion"),
        ("Away + High Priority", "away", "high", "proposal")
    ]
    
    for scenario_name, status, priority, phase in auto_reply_scenarios:
        print(f"\n--- {scenario_name} ---")
        auto_reply = agent.generate_auto_reply(status, priority, phase)
        
        print(f"Subject: {auto_reply['subject']}")
        print(f"Estimated Response: {auto_reply['estimated_response']}")
        print(f"Body Preview: {auto_reply['body'][:150]}...")
        print(f"Status: {auto_reply['sender_status']} | Priority: {auto_reply['priority_level']}")
    
    print("\n" + "="*50)