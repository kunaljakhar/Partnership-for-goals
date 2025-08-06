from transformers import pipeline

class CommunicationAgent:
    def __init__(self):
        self.gen = pipeline("text-generation", model="gpt2")
        self.tone_classifier = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emotion")

    def compose_message(self, context, formality="formal"):
        prompt = f"Write a {formality} email: {context}"
        result = self.gen(prompt, max_length=100, eos_token_id=50256)
        return result[0]['generated_text']

    def analyze_tone(self, message):
        result = self.tone_classifier(message)
        return result
