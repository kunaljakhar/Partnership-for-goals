from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class DiscoveryAgent:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed(self, text):
        tokens = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            output = self.model(**tokens)
        embeddings = output.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
        return embeddings

    def match_projects(self, user_skills, projects):
        user_emb = self.embed(" ".join(user_skills))
        scores = []
        for project in projects:
            project_emb = self.embed(" ".join(project['skills']))
            similarity = float(np.dot(user_emb, project_emb) / (np.linalg.norm(user_emb) * np.linalg.norm(project_emb)))
            scores.append({'project': project, 'similarity': similarity})
        scores.sort(key=lambda x: x['similarity'], reverse=True)
        return scores
