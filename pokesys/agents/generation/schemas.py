from typing import Union
from pydantic import BaseModel


class DefaultResponse(BaseModel):
    answer: str


class BaseStats(BaseModel):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class PokemonStatsResponse(BaseModel):
    name: str
    base_stats: BaseStats


class PokemonBattleResponse(BaseModel):
    reasoning: str
    answer: str
    winner: str


class SupervisorResponse(BaseModel):
    response: Union[
        DefaultResponse, 
        PokemonStatsResponse, 
        PokemonBattleResponse
    ]
