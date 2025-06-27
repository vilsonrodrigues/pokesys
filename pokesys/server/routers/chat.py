from typing import Union
from fastapi import APIRouter
from pokesys.server.schemas.chat import ChatDefaultResponse, ChatPokemonStatsResponse, ChatRequest
from pokesys.workflow import run_workflow_async


router = APIRouter()

@router.post("/chat", tags=["chat"], response_model=Union[ChatDefaultResponse, ChatPokemonStatsResponse])
async def chat(query: ChatRequest):    
    question = query.question
    response = await run_workflow_async(question)
    response.pop("winner", None)
    return response
