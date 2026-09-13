
import re
from typing import List, Dict, Any
from utils.nlp_basic import extract_sentence, parse_number

# ------------------------------
# REGEX CANDIDATE EXTRACTION
# ------------------------------
NUM_RE = r"(?:\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d+)?|\d+(?:[.,]\d+)?)"
PCT_RE = rf"({NUM_RE})\s*%|\b({NUM_RE})\s*points\b"
MONEY_RE = rf"({NUM_RE})\s*(€|euros|EUR|dollars|USD|k€|M€|millions?)"
UNIT_RE = rf"({NUM_RE})\s*(kWh|GWh|kW|MW|k|M|t|tonnes|m²|m2|ha|jours|j|heures|h|min|%)\b"
GENERIC_NUM_RE = rf"({NUM_RE})"

def regex_extract_candidates(text: str) -> List[Dict[str, Any]]:
    candidates = []
    # percentages & "points"
    for m in re.finditer(PCT_RE, text, flags=re.IGNORECASE):
        val = m.group(1) or m.group(2)
        span = m.span()
        candidates.append({
            "raw_value": val,
            "unit": "%",
            "match": m.group(0),
            "start": span[0],
            "end": span[1],
            "sentence": extract_sentence(text, span[0]),
            "method": "regex_pct",
            "score": 0.9
        })
    # units
    for m in re.finditer(UNIT_RE, text, flags=re.IGNORECASE):
        val = m.group(1)
        unit = m.group(2)
        span = m.span()
        candidates.append({
            "raw_value": val,
            "unit": unit,
            "match": m.group(0),
            "start": span[0],
            "end": span[1],
            "sentence": extract_sentence(text, span[0]),
            "method": "regex_unit",
            "score": 0.85
        })
    # money
    for m in re.finditer(MONEY_RE, text, flags=re.IGNORECASE):
        val = m.group(1)
        unit = m.group(2)
        span = m.span()
        candidates.append({
            "raw_value": val,
            "unit": unit,
            "match": m.group(0),
            "start": span[0],
            "end": span[1],
            "sentence": extract_sentence(text, span[0]),
            "method": "regex_money",
            "score": 0.88
        })
    # generic numbers
    for m in re.finditer(GENERIC_NUM_RE, text, flags=re.IGNORECASE):
        span = m.span()
        # avoid overlaps
        if any(abs(span[0]-c["start"]) < 5 for c in candidates):
            continue
        val = m.group(1)
        candidates.append({
            "raw_value": val,
            "unit": None,
            "match": m.group(0),
            "start": span[0],
            "end": span[1],
            "sentence": extract_sentence(text, span[0]),
            "method": "regex_num",
            "score": 0.5
        })
    # deduplicate by start keeping highest score
    best = {}
    for c in candidates:
        s = c["start"]
        if s not in best or c["score"] > best[s]["score"]:
            best[s] = c
    return list(best.values())

# ------------------------------
# NORMALIZATION
# ------------------------------


def normalize_candidate(c: Dict[str,Any]) -> Dict[str,Any]:
    v = parse_number(c.get("raw_value"))
    unit = c.get("unit")
    # unify percent
    if unit and unit.strip() == '%':
        pass
    # unify tonnes
    if unit and unit.lower() in ['t','tonnes']:
        unit = 'tonnes'
    return {**c, "value": v, "unit_norm": unit}
