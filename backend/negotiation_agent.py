from transformers import pipeline

class NegotiationAgent:
    def __init__(self):
        self.sim_checker = pipeline("text-classification", model="sentence-transformers/paraphrase-MiniLM-L6-v2")

    def analyze_and_counter(self, expected_terms, proposed_terms):
        results = []
        for expected, proposed in zip(expected_terms, proposed_terms):
            sim = self.sim_checker(f"{expected} [SEP] {proposed}")[0]['score']
            if sim > 0.7:
                results.append({'status': 'Accepted', 'proposed': proposed})
            else:
                results.append({'status': 'Counter', 'suggested': expected})
        return results
