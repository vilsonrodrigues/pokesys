from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Model Request for chat endpoint."""
    question: str


class ChatDefaultResponse(BaseModel):
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


class ChatPokemonStatsResponse(BaseModel):
    """Model response for Pokemon data."""
    name: str
    base_stats: PokemonStats
