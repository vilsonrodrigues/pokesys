import pytest
from pokesys.agents.tools.expert import (
    get_type_multiplier,
    estimate_damage,
    decide_winner
)

# Testes para get_type_multiplier

@pytest.mark.parametrize("attack_type, defender_types, expected", [
    ("electric", ["water"], 2.0),    # super efetivo
    ("fire", ["grass"], 2.0),
    ("electric", ["ground"], 0.5),   # fraco contra
    ("normal", ["ghost"], 0.0),      # imune
    ("grass", ["fire"], 0.5),
    ("bug", ["fire", "flying"], 0.25),  # duplamente fraco
])
def test_get_type_multiplier(attack_type, defender_types, expected):
    result = get_type_multiplier(attack_type, defender_types)
    assert result == expected


# Testes para estimate_damage

def test_estimate_damage_simple_case():
    attacker = {
        "base_stats": {"attack": 80, "special_attack": 100},
        "types": ["fire"]
    }
    defender = {
        "base_stats": {"defense": 60, "special_defense": 80},
        "types": ["grass"]
    }
    result = estimate_damage(attacker, defender)
    expected_attack = 100  # special_attack maior
    expected_defense = 60  # menor defesa
    expected_multiplier = 2.0  # fogo > grama
    expected_damage = (100 / 60) * 2.0
    assert result == pytest.approx(expected_damage)


# Testes para decide_winner

def test_decide_winner_strong_vs_weak():
    charizard = {
        "name": "charizard",
        "base_stats": {"attack": 84, "special_attack": 109, "defense": 78, "special_defense": 85},
        "types": ["fire", "flying"]
    }
    venusaur = {
        "name": "venusaur",
        "base_stats": {"attack": 82, "special_attack": 100, "defense": 83, "special_defense": 100},
        "types": ["grass", "poison"]
    }

    result = decide_winner(charizard, venusaur)
    assert result["winner"] == "charizard"
    assert "Charizard has a likely advantage" in result["reasoning"]
