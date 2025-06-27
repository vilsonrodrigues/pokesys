from pydantic import BaseModel, Field


class BattleResponse(BaseModel):
    """Model response for Battle."""
    reasoning: str = Field(..., description="Reasoning for why this Pokemon was the winner")
    winner: str = Field(..., description="Name of the winning Pokemon")
