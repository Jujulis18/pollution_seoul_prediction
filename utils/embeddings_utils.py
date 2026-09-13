
import numpy as np

from sentence_transformers import SentenceTransformer

import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer, util
from utils.nlp_basic import infer_kpi_name_from_snippet, infer_trend_from_sentence

# ------------------------------
# EMBEDDING-BASED CLASSIFICATION
# ------------------------------
embedder = None
if SentenceTransformer is not None:
    try:
        embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    except Exception:
        embedder = None

# anchor prototypes for broad categories
ANCHORS = {
    "Finance": ["revenue", "cost", "budget", "expense", "profit", "CA", "dépense"],
    "Health": ["patient", "hospitalization", "admission", "re-admission", "infection", "morbidity"],
    "Environment": ["emission", "CO2", "pollution", "air quality", "recycling", "energy"],
    "Mobility": ["transport", "traffic", "commute", "transit", "bus", "tram"],
    "Citizen": ["satisfaction", "user", "report", "complaint", "engagement"],
    "Operations": ["uptime", "latency", "throughput", "performance", "efficiency"]
}

# simple anchor keywords (used if no embeddings)
KPI_KEYWORDS = {
    "finance": ["chiffre d'affaires", "budget", "coût", "dépense", "revenu", "€/€", "milliards", "millions"],
    "health": ["patient", "hospitalisation", "séjour", "réadmission", "infection", "taux de mortalité"],
    "environment": ["émission", "co2", "pm2.5", "pollution", "recyclage", "énergie", "kwh"],
    "mobility": ["transport", "mobilité", "trajet", "bus", "tram", "vélo"],
    "citizen": ["satisfaction", "utilisateur", "signalement", "usager", "résolution"],
    "iot": ["capteur", "iot", "borne", "déploiement"]
}

anchor_embeddings = None
if embedder is not None:
    anchor_texts = ["; ".join(v) for v in ANCHORS.values()]
    anchor_embeddings = embedder.encode(anchor_texts, convert_to_tensor=True, normalize_embeddings=True)

def classify_by_embedding(snippet: str) -> str:
    if embedder is None or anchor_embeddings is None:
        # fallback keyword matching
        s = snippet.lower()
        for cat, kws in KPI_KEYWORDS.items():
            for kw in kws:
                if kw.lower() in s:
                    return cat
        return "other"
    emb = embedder.encode([snippet], convert_to_tensor=True, normalize_embeddings=True)
    sims = util.cos_sim(emb, anchor_embeddings)[0].cpu().numpy()
    # find best anchor
    best_idx = int(np.argmax(sims))
    return list(ANCHORS.keys())[best_idx]

# ------------------------------
# SCORING, INFERENCE, MERGE
# ------------------------------


def merge_and_score(regex_norm: List[Dict[str,Any]], llm_structs: List[Dict[str,Any]]) -> List[Dict[str,Any]]:
    # map sentences -> LLM extractions
    sentence_to_llm = {}
    for l in llm_structs:
        sentence_to_llm.setdefault(l.get("sentence",""), []).append(l)
    out = []
    for c in regex_norm:
        sentence = c.get("sentence","")
        llm_here = sentence_to_llm.get(sentence, [])
        # prefer LLM name if present else infer
        if llm_here:
            name = llm_here[0].get("name") or llm_here[0].get("kpi") or None
            unit = llm_here[0].get("unit") or c.get("unit_norm")
            value = llm_here[0].get("value") if llm_here[0].get("value") is not None else c.get("value")
            conf = min(1.0, c.get("score",0.5) + llm_here[0].get("confidence",0.8)*0.4)
        else:
            name = infer_kpi_name_from_snippet(sentence)
            unit = c.get("unit_norm")
            value = c.get("value")
            conf = c.get("score", 0.5)
        category = classify_by_embedding(sentence)
        trend = infer_trend_from_sentence(sentence)
        out.append({
            "kpi_name": name or "Indicateur",
            "raw_value": c.get("raw_value"),
            "value": value,
            "unit": unit,
            "sentence": sentence,
            "start": c.get("start"),
            "confidence": round(float(conf),3),
            "category": category,
            "trend": trend
        })
    return out