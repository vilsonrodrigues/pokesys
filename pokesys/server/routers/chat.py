from fastapi import APIRouter
from pokesys.server.schemas import ChatRequest
from pokesys.workflow import run_workflow_async


router = APIRouter()

@router.post("/chat", tags=["chat"])
async def chat(query: ChatRequest):    
    question = query.question
    response = run_workflow_async(question)
    response.pop("winner", None)
    return response
