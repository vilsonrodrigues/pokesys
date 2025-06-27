from fastapi import APIRouter, Query
from pokesys.workflow import run_workflow_async


router = APIRouter()

@router.get("/battle", tags=["battle"])
async def battle(pokemon1: str = Query(...), pokemon2: str = Query(...)):
    question = f"Who would win a battle between {pokemon1} and {pokemon2}?"
    response = await run_workflow_async(question)
    response.pop("answer", None)
    return response
