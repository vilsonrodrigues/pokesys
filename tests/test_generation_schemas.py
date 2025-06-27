import pytest
from pydantic import ValidationError
from pokesys.agents.generation.schemas import (
    DefaultResponse,
    BaseStats,
    PokemonStatsResponse,
    PokemonBattleResponse,
    SupervisorResponse,
)


def test_default_response_valid():
    response = DefaultResponse(answer="This is a valid response")
    assert response.answer == "This is a valid response"


def test_default_response_invalid_type():
    with pytest.raises(ValidationError, match="Input should be a valid string"):
        DefaultResponse(answer=123)

def test_base_stats_valid():
    stats = BaseStats(
        hp=100,
        attack=80,
        defense=90,
        special_attack=70,
        special_defense=60,
        speed=50,
    )
    assert stats.hp == 100
    assert stats.attack == 80
    assert stats.defense == 90
    assert stats.special_attack == 70
    assert stats.special_defense == 60
    assert stats.speed == 50


def test_base_stats_invalid_type():
    with pytest.raises(ValidationError, match="Input should be a valid integer"):
        BaseStats(
            hp="invalid",
            attack=80,
            defense=90,
            special_attack=70,
            special_defense=60,
            speed=50,
        )


def test_base_stats_negative_values():
    stats = BaseStats(
        hp=-10,
        attack=80,
        defense=90,
        special_attack=70,
        special_defense=60,
        speed=50,
    )
    assert stats.hp == -10

def test_pokemon_stats_response_valid():
    stats = BaseStats(
        hp=100, attack=80, defense=90, special_attack=70, special_defense=60, speed=50
    )
    response = PokemonStatsResponse(name="Pikachu", base_stats=stats)
    assert response.name == "Pikachu"
    assert response.base_stats == stats
    assert response.base_stats.hp == 100


def test_pokemon_stats_response_invalid_name():
    stats = BaseStats(
        hp=100, attack=80, defense=90, special_attack=70, special_defense=60, speed=50
    )
    with pytest.raises(ValidationError, match="Input should be a valid string"):
        PokemonStatsResponse(name=123, base_stats=stats)


def test_pokemon_stats_response_invalid_base_stats():
    with pytest.raises(ValidationError, match="Input should be a valid integer"):
        PokemonStatsResponse(name="Pikachu", base_stats={"hp": "invalid"})


def test_pokemon_battle_response_valid():
    response = PokemonBattleResponse(
        reasoning="Pikachu wins due to speed advantage.",
        answer="Pikachu is the winner.",
        winner="Pikachu",
    )
    assert response.reasoning == "Pikachu wins due to speed advantage."
    assert response.answer == "Pikachu is the winner."
    assert response.winner == "Pikachu"


def test_pokemon_battle_response_invalid_type():
    with pytest.raises(ValidationError, match="Input should be a valid string"):
        PokemonBattleResponse(
            reasoning=123,
            answer="Pikachu is the winner.",
            winner="Pikachu",
        )


def test_supervisor_response_with_default_response():
    default_response = DefaultResponse(answer="This is a valid response")
    supervisor_response = SupervisorResponse(response=default_response)
    assert isinstance(supervisor_response.response, DefaultResponse)
    assert supervisor_response.response.answer == "This is a valid response"


def test_supervisor_response_with_pokemon_stats_response():
    stats = BaseStats(
        hp=100, attack=80, defense=90, special_attack=70, special_defense=60, speed=50
    )
    pokemon_response = PokemonStatsResponse(name="Pikachu", base_stats=stats)
    supervisor_response = SupervisorResponse(response=pokemon_response)
    assert isinstance(supervisor_response.response, PokemonStatsResponse)
    assert supervisor_response.response.name == "Pikachu"
    assert supervisor_response.response.base_stats.hp == 100


def test_supervisor_response_with_pokemon_battle_response():
    battle_response = PokemonBattleResponse(
        reasoning="Pikachu wins due to speed advantage.",
        answer="Pikachu is the winner.",
        winner="Pikachu",
    )
    supervisor_response = SupervisorResponse(response=battle_response)
    assert isinstance(supervisor_response.response, PokemonBattleResponse)
    assert supervisor_response.response.winner == "Pikachu"


def test_supervisor_response_invalid_response_type():
    with pytest.raises(ValidationError, match="Field required"):
        SupervisorResponse(response={"invalid": "data"})


def test_supervisor_response_none_response():
    with pytest.raises(ValidationError, match="Input should be a valid dictionary or instance of"):
        SupervisorResponse(response=None)