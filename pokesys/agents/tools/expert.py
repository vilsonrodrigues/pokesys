from typing import Any, Dict, List

# https://www.poke-blast-news.net/2022/12/tipos-pokemon-vantagens-e-fraquezas.html
type_chart = {
    "normal": {
        "strong": [],
        "weak": ["fighting"],
        "immune": ["ghost"]
    },
    "grass": {
        "strong": ["ground", "rock", "water"],
        "weak": ["bug", "fire", "flying", "ice", "poison"],
        "immune": []
    },
    "fire": {
        "strong": ["bug", "grass", "ice", "steel"],
        "weak": ["rock", "ground", "water"],
        "immune": []
    },
    "water": {
        "strong": ["fire", "ground", "rock"],
        "weak": ["electric", "grass"],
        "immune": []
    },
    "electric": {
        "strong": ["water", "flying"],
        "weak": ["ground"],
        "immune": []
    },
    "flying": {
        "strong": ["bug", "fighting", "grass"],
        "weak": ["electric", "ice", "rock"],
        "immune": ["ground"]
    },
    "ice": {
        "strong": ["dragon", "flying", "grass", "ground"],
        "weak": ["fighting", "fire", "rock", "steel"],
        "immune": []
    },
    "rock": {
        "strong": ["bug", "fire", "flying", "ice"],
        "weak": ["fighting", "grass", "ground", "steel", "water"],
        "immune": []
    },
    "ground": {
        "strong": ["electric", "fire", "poison", "rock", "steel"],
        "weak": ["ice", "grass", "water"],
        "immune": ["electric"]
    },
    "steel": {
        "strong": ["fairy", "ice", "rock"],
        "weak": ["fighting", "fire", "ground"],
        "immune": ["poison"]
    },
    "fighting": {
        "strong": ["dark", "ice", "normal", "rock", "steel"],
        "weak": ["fairy", "flying", "psychic"],
        "immune": []
    },
    "dark": {
        "strong": ["ghost", "psychic"],
        "weak": ["bug", "fairy", "fighting"],
        "immune": ["psychic"]
    },
    "psychic": {
        "strong": ["fighting", "poison"],
        "weak": ["bug", "dark", "ghost"],
        "immune": []
    },
    "poison": {
        "strong": ["fairy", "grass"],
        "weak": ["ground", "psychic"],
        "immune": []
    },
    "bug": {
        "strong": ["dark", "grass", "psychic"],
        "weak": ["fire", "flying", "rock"],
        "immune": []
    },
    "fairy": {
        "strong": ["dark", "dragon", "fighting"],
        "weak": ["steel", "poison"],
        "immune": ["dragon"]
    },
    "ghost": {
        "strong": ["ghost", "psychic"],
        "weak": ["dark", "ghost"],
        "immune": ["normal", "fighting"]
    },
    "dragon": {
        "strong": ["dragon"],
        "weak": ["dragon", "fairy", "ice"],
        "immune": []
    }
}

def get_type_multiplier(attack_type: str, defender_types: List[str]) -> float:
    """Calculates the type effectiveness multiplier of an attack against a defender.

    Args:
        attack_type (str): The type of the attacking Pokémon (e.g., 'electric').
        defender_types (list[str]): A list of types of the defending Pokémon.

    Returns:
        The effectiveness multiplier (e.g., 2.0 for super effective, 
        0.5 for not very effective, 0.0 for immune).
    """
    multiplier = 1.0
    for dtype in defender_types:
        if dtype in type_chart[attack_type]["strong"]:
            multiplier *= 2.0
        elif dtype in type_chart[attack_type]["weak"]:
            multiplier *= 0.5
        elif dtype in type_chart[attack_type]["immune"]:
            multiplier *= 0.0
    return multiplier

def estimate_damage(attacker: Dict[str, Any], defender: Dict[str, Any]) -> float:
    """Estimates the relative damage one Pokémon can inflict on another.

    It selects the highest offensive stat (attack or special_attack) of the attacker
    and the lowest defensive stat (defense or special_defense) of the defender,
    applying the best type effectiveness multiplier available.

    Args:
        attacker: A dictionary containing 'base_stats' and 'types' for the attacking Pokémon.
        defender: A dictionary containing 'base_stats' and 'types' for the defending Pokémon.

    Returns:
        The estimated damage ratio attacker would deal to the defender.
    """
    best_attack = max(attacker["base_stats"]["attack"], attacker["base_stats"]["special_attack"])
    best_defense = min(defender["base_stats"]["defense"], defender["base_stats"]["special_defense"])
    type_multipliers = [
        get_type_multiplier(atk_type, defender["types"])
        for atk_type in attacker["types"]
    ]
    best_multiplier = max(type_multipliers)
    return (best_attack / best_defense) * best_multiplier

def decide_winner(pokemon1_data: Dict[str, Any], pokemon2_data: Dict[str, Any]) -> Dict[str, Any]:
    """Determines the likely winner between two Pokémon based on stats and type matchups.

    Args:
        pokemon1_data: The first Pokémon's data, including base stats and types.
        pokemon2_data: The second Pokémon's data, including base stats and types.

    Returns:
        A dict containing:
            - The name of the likely winner (or None if evenly matched).
            - A human-readable explanation of the decision.
    """    
    damage1 = estimate_damage(pokemon1_data, pokemon2_data)
    damage2 = estimate_damage(pokemon2_data, pokemon1_data)

    explanation = f"{pokemon1_data['name'].capitalize()} would cause approximately {damage1:.2f} of damage to {pokemon2_data['name'].capitalize()}, "
    explanation += f"while {pokemon2_data['name'].capitalize()} would cause {damage2:.2f} of damage to {pokemon1_data['name'].capitalize()}."

    if damage1 > damage2:
        explanation += f"Therefore, {pokemon1_data['name'].capitalize()} has a likely advantage in battle."
        winner = pokemon1_data["name"]
    elif damage2 > damage1:
        explanation += f"Therefore, {pokemon2_data['name'].capitalize()} has a likely advantage in battle."
        winner = pokemon2_data["name"]
    else:
        explanation += "The battle seems balanced."
        winner = None

    response = {"reasoning": explanation, "winner": winner}
    return response

EXPERT_TOOLS = [decide_winner]
