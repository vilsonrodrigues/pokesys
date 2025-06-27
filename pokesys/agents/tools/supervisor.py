import requests
from typing import List, Dict


def get_pokemon_lore(pokemon_name: str) -> Dict[str, str]:
    """
    Retrieves and assembles basic lore information about a given Pokémon
    using the PokeAPI. It includes flavor text, habitat, generation, 
    legendary/mythical status, and evolution chain.

    Args:
        pokemon_name: Pokemon name to retrieve information for.

    Returns:
        A formatted string containing the lore and biological background 
        of the Pokemon. If the Pokémon is not found, returns an error message.
    """
    base_url = "https://pokeapi.co/api/v2"
    species_url = f"{base_url}/pokemon-species/{pokemon_name.lower()}"

    response = requests.get(species_url)
    if response.status_code != 200:
        return f"Error: Pokemon `{pokemon_name}` not found."

    species_data: Dict = response.json()

    # Extract English flavor texts
    flavor_texts: List[str] = [
        entry["flavor_text"].replace("\n", " ").replace("\f", " ")
        for entry in species_data["flavor_text_entries"]
        if entry["language"]["name"] == "en"
    ]
    unique_texts: List[str] = list(dict.fromkeys(flavor_texts))  # Deduplicate

    # Habitat
    habitat: str = species_data["habitat"]["name"].capitalize() if species_data["habitat"] else "Unknown"

    # Generation
    generation: str = species_data["generation"]["name"].replace("generation-", "").upper()

    # Legendary or mythical status
    if species_data["is_legendary"]:
        status = "Legendary"
    elif species_data["is_mythical"]:
        status = "Mythical"
    else:
        status = "Common"

    # Evolution chain
    evolution_url = species_data["evolution_chain"]["url"]
    evolution_response = requests.get(evolution_url)
    evolution_data: Dict = evolution_response.json()

    def extract_evolution_chain(chain_node: Dict) -> List[str]:
        """Recursively extract evolution names from the evolution chain."""
        names = [chain_node["species"]["name"]]
        for evolution in chain_node.get("evolves_to", []):
            names.extend(extract_evolution_chain(evolution))
        return names

    evolution_chain = extract_evolution_chain(evolution_data["chain"])

    # Assemble the lore text
    lore = f"Pokemon Lore: {pokemon_name.capitalize()}\n"
    lore += f"Status: {status}\n"
    lore += f"Habitat: {habitat}\n"
    lore += f"Generation: {generation}\n"
    lore += f"Evolution Chain: {' -> '.join(name.capitalize() for name in evolution_chain)}\n\n"
    lore += "Pokedex Entries:\n"
    for _, entry in enumerate(unique_texts[:3]):  # Limit to 3 entries
        lore += f"  - {entry}\n"
    response = {"answer": lore}
    return response

SUPERVISOR_TOOLS = [get_pokemon_lore]