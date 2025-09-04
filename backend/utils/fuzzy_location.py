from thefuzz import process

# Synonyms for common abbreviations or misspellings
SYNONYMS = {
    "mel": "melbourne",
    "melboune": "melbourne",
    "rich": "richmond",
    "carl": "carlton"
}

def _normalize_location_name(name: str) -> str:
    """
    Normalize location names using synonyms and lowercase cleanup
    """
    name = name.lower().strip()
    return SYNONYMS.get(name, name)


def _fuzzy_match_location(query: str, location_list: list, threshold: int = 70) -> str:
    """
    Fuzzy match a location from the list. Returns the best match if score >= threshold.
    """
    query = _normalize_location_name(query)
    match, score = process.extractOne(query, location_list)
    if score >= threshold:
        return match
    return None
