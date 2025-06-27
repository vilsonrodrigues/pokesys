from typing import Union, TypedDict


class DefaultResponse(TypedDict):
    answer: str


class BaseStats(TypedDict):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class PokemonStatsResponse(TypedDict):
    name: str
    base_stats: BaseStats


class PokemonBattleResponse(TypedDict):
    reasoning: str
    answer: str
    winner: str


class SupervisorResponse(TypedDict):
    response: Union[
        DefaultResponse, 
        PokemonStatsResponse, 
        PokemonBattleResponse
    ]
