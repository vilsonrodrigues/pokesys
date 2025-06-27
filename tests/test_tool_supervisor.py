import pytest
import requests
from pokesys.agents.tools.supervisor import get_pokemon_lore


def test_get_pokemon_lore_not_found(requests_mock):
    requests_mock.get("https://pokeapi.co/api/v2/pokemon-species/missingno", status_code=404)
    result = get_pokemon_lore("missingno")
    assert result == "Error: Pokemon `missingno` not found."


def test_get_pokemon_lore_success(requests_mock):
    species_url = "https://pokeapi.co/api/v2/pokemon-species/pikachu"
    evolution_url = "https://pokeapi.co/api/v2/evolution-chain/10"

    # Mock species response
    species_payload = {
        "flavor_text_entries": [
            {"flavor_text": "When several of these Pokémon gather, their electricity could build and cause lightning storms.",
             "language": {"name": "en"}},
            {"flavor_text": "Quando vários deles se reúnem, causam tempestades.", "language": {"name": "pt"}}
        ],
        "habitat": {"name": "forest"},
        "generation": {"name": "generation-i"},
        "is_legendary": False,
        "is_mythical": False,
        "evolution_chain": {"url": evolution_url}
    }
    requests_mock.get(species_url, json=species_payload)

    # Mock evolution chain response
    evolution_payload = {
        "chain": {
            "species": {"name": "pichu"},
            "evolves_to": [{
                "species": {"name": "pikachu"},
                "evolves_to": [{
                    "species": {"name": "raichu"},
                    "evolves_to": []
                }]
            }]
        }
    }
    requests_mock.get(evolution_url, json=evolution_payload)

    result = get_pokemon_lore("pikachu")
    assert isinstance(result, dict)
    assert "answer" in result
    text = result["answer"]
    assert "Pikachu" in text
    assert "Habitat: Forest" in text
    assert "Generation: I" in text
    assert "Status: Common" in text
    assert "Pichu -> Pikachu -> Raichu" in text
    assert "Pokedex Entries" in text
