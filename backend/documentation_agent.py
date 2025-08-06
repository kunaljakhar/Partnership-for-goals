from transformers import pipeline

class DocumentationAgent:
    def __init__(self):
        self.gen = pipeline("text-generation", model="gpt2")

    def draft_mou(self, parties, project, terms):
        prompt = f"Draft a Memorandum of Understanding between {parties} for {project} with these terms: {terms}"
        result = self.gen(prompt, max_length=200, eos_token_id=50256)
        return result[0]['generated_text']

    def draft_letter(self, recipient, subject, content):
        prompt = f"Write an acceptance letter to {recipient} about {subject}: {content}"
        result = self.gen(prompt, max_length=120, eos_token_id=50256)
        return result[0]['generated_text']
