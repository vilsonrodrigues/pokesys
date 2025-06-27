import pytest
from pydantic import ValidationError
from pokesys.server.schemas.chat import (
    ChatRequest,
    ChatDefaultResponse,
    PokemonStats,
    ChatPokemonStatsResponse
)


def test_chat_request_valid():
    request = ChatRequest(question="Who would win, Charizard or Blastoise?")
    assert request.question == "Who would win, Charizard or Blastoise?"


def test_chat_request_missing_question():
    with pytest.raises(ValidationError):
        ChatRequest()


def test_chat_default_response_valid():
    response = ChatDefaultResponse(reasoning="Water beats fire.", answer="Blastoise")
    assert response.reasoning == "Water beats fire."
    assert response.answer == "Blastoise"


def test_chat_default_response_no_reasoning():
    response = ChatDefaultResponse(answer="Bulbasaur")
    assert response.reasoning is None
    assert response.answer == "Bulbasaur"


def test_pokemon_stats_and_response():
    stats = PokemonStats(
        hp=80,
        attack=82,
        defense=83,
        special_attack=100,
        special_defense=100,
        speed=80
    )
    response = ChatPokemonStatsResponse(name="Venusaur", base_stats=stats)
    assert response.name == "Venusaur"
    assert response.base_stats.hp == 80
    assert response.base_stats.special_attack == 100


def test_invalid_pokemon_stats():
    with pytest.raises(ValidationError):
        PokemonStats(
            hp="high",  # invalid type
            attack=82,
            defense=83,
            special_attack=100,
            special_defense=100,
            speed=80
        )
