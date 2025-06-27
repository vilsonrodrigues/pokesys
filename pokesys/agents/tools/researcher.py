import requests
from typing import Any, Dict, List
from langchain_core.tools import tool
from pokesys.executor import scatter_gather


def get_pokemon_data(pokemon_name: str) -> Dict[str, Any]:
    """
    Get Pokemon data from PokéAPI

    Args:
        pokemon_name: Pokemon name.

    Returns:
        Pokemon data.
    """
    name = pokemon_name.lower().strip() # lowercase, remove spaces

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")

    if response.status_code == 200:
        data = response.json()

        pokemon_info = {
            "name": data["name"],
            "base_stats": {
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "defense": data["stats"][2]["base_stat"],
                "special_attack": data["stats"][3]["base_stat"],
                "special_defense": data["stats"][4]["base_stat"],
                "speed": data["stats"][5]["base_stat"],
            },
            "types": [t["type"]["name"] for t in data["types"]],
        }
        return pokemon_info
    else:
        return {"error": f"Pokemon `{pokemon_name}` not found."}

def get_pokemon_info(pokemon_name: str) -> Dict[str, Any]:
    """
    Get info about a Pokemon from the PokeAPI.

    Args:
        pokemon_name: Pokemon name.

    Returns:
        Dictionary containing the Pokemon data.
    """
    try:
        return get_pokemon_data(pokemon_name)
    except Exception as e:
        return {"error": str(e)}

@tool(return_direct=True)
def get_pokemons_info(pokemon_names: List[str]) -> List[Dict[str, Any]]:
    """
    Get information about a list of Pokemon from the PokeAPI.

    Args:
        pokemon_names: List of Pokemon names.

    Returns:
        List of dict containing Pokemon data.
    """
    to_send = [get_pokemon_info] * len(pokemon_names)
    args_list = [(name,) for name in pokemon_names]
    response = scatter_gather(to_send=to_send, args_list=args_list)
    return list(response)

RESEARCHER_TOOLS = [get_pokemon_info]
