from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from backend.controller import MultiAgentController
import db_helpers

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
controller = MultiAgentController()

# Allow all origins for testing - restrict this in prod!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Pydantic models for request/response
class Project(BaseModel):
    id: int
    name: str
    skills: List[str]

class MatchRequest(BaseModel):
    user_id: int
    user_skills: List[str]
    projects: List[Project]

class NegotiationRequest(BaseModel):
    match_id: int
    expected_terms: List[str]
    proposed_terms: List[str]

class CommunicationRequest(BaseModel):
    negotiation_id: int
    context: str
    formality: str = "formal"

class DocumentRequest(BaseModel):
    negotiation_id: int
    doc_type: str  # e.g., 'mou' or 'letter'
    parties: str = ""
    project: str = ""
    terms: str = ""
    recipient: str = ""
    subject: str = ""
    content: str = ""

@app.post("/match-projects")
def match_projects(data: MatchRequest):
    scores = controller.discovery.match_projects(
        data.user_skills,
        [proj.dict() for proj in data.projects]
    )
    # Save top match
    for match in scores[:3]:
        project_id = match['project'].get('id')
        sim = match['similarity']
        db_helpers.save_match(data.user_id, project_id, sim)
    return scores

@app.post("/negotiate")
def negotiate_terms(data: NegotiationRequest):
    result = controller.negotiation.analyze_and_counter(
        data.expected_terms, data.proposed_terms
    )
    negotiation_id = db_helpers.save_negotiation(
        data.match_id, data.expected_terms, data.proposed_terms, result)
    return {"result": result, "negotiation_id": negotiation_id}

@app.post("/compose-message")
def compose_message(data: CommunicationRequest):
    msg = controller.communication.compose_message(
        data.context, formality=data.formality
    )
    tone = controller.communication.analyze_tone(msg)
    comm_id = db_helpers.save_communication(
        data.negotiation_id, msg, tone)
    return {"message": msg, "tone": tone, "communication_id": comm_id}

@app.post("/generate-document")
def generate_document(data: DocumentRequest):
    if data.doc_type == "mou":
        content = controller.documentation.draft_mou(data.parties, data.project, data.terms)
    elif data.doc_type == "letter":
        content = controller.documentation.draft_letter(data.recipient, data.subject, data.content)
    else:
        content = "Invalid doc_type"
    doc_id = db_helpers.save_document(
        data.negotiation_id, data.doc_type, content)
    return {"document": content, "document_id": doc_id}
