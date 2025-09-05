from thefuzz import process

# Synonyms for common abbreviations / misspellings
SYNONYMS = {
    "mel": "melbourne",
    "melb": "melbourne",
    "melboune": "melbourne",
    "rich": "richmond",
    "carl": "carlton"
}

def _normalize_location_name(name: str) -> str:
    """Lowercase + trim + synonym map."""
    name = (name or "").lower().strip()
    return SYNONYMS.get(name, name)

def _fuzzy_match_location(query: str, candidates: list, threshold: int = 70):
    """Return (best_match, score) if score >= threshold, else (None, 0)."""
    query = _normalize_location_name(query)
    match, score = process.extractOne(query, candidates)
    return (match, score) if score >= threshold else (None, 0)

def resolve_location_to_coords(query: str, coords_by_name: dict, threshold: int = 70):
    """Resolve a user query into coordinates, using exact or fuzzy matching."""
    q = _normalize_location_name(query)

    # Exact match first
    if q in coords_by_name:
        return coords_by_name[q], "exact", 100, q

    # Fuzzy fallback
    names = list(coords_by_name.keys())
    match, score = _fuzzy_match_location(q, names, threshold)
    if match:
        return coords_by_name[match], "fuzzy", score, match

    return None, "none", 0, None
