from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Model Request for chat endpoint."""
    question: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    reasoning: Optional[str] = Field(None, description="Reasoning behind the answer")
    answer: str


class PokemonStats(BaseModel):
    """Model response for Pokemon base stats."""
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class PokemonStatsResponse(BaseModel):
    """Model response for Pokemon data."""
    name: str
    base_stats: PokemonStats


class BattleResponse(BaseModel):
    """Model response for Battle."""
    reasoning: str = Field(..., description="Reasoning for why this Pokemon was the winner")
    winner: str = Field(..., description="Name of the winning Pokemon")
