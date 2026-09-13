
import streamlit as st
from transformers import pipeline

import json
from typing import List, Dict, Any
# ------------------------------
# LLM STRUCTURING (Mistral via HF pipeline)
# ------------------------------
def load_mistral_pipeline(model_name: str):
    if pipeline is None:
        return None
    try:
        # For instruction-style models prefer text-generation / text2text depending on model
        # We use text-generation with an instruct prompt.
        gen = pipeline("text-generation", model=model_name, device=0 if (st.runtime and hasattr(st.runtime, "device")) else -1, max_new_tokens=512, do_sample=False)
        return gen
    except Exception as e:
        st.warning(f"Impossible de charger Mistral HF pipeline ({model_name}): {e}")
        return None

def llm_structured_extraction(mistral_gen, sentences: List[str], top_k: int = 8) -> List[Dict[str,Any]]:
    """
    Call Mistral to extract KPI records from sentences.
    Expects mistral_gen from transformers.pipeline (text-generation).
    Returns list of dicts: {name, value, unit, period, note, confidence}
    """
    if mistral_gen is None:
        return []
    results = []
    # prompt template - instruct model to return strict JSON array
    prompt_template = (
        "You are a data assistant. Extract KPI information from the following sentence. "
        "Return a JSON array of objects with fields: name, value (numeric if possible), unit, period (if present), note. "
        "If no KPI, return [] ."
        "Sentence: "
    )
    for s in sentences[:top_k]:
        prompt = prompt_template + json.dumps(s, ensure_ascii=False)
        try:
            out = mistral_gen(prompt, max_new_tokens=320)[0]["generated_text"]
        except Exception as e:
            out = ""
        parsed = parse_json_like(out)
        if isinstance(parsed, list):
            for p in parsed:
                p['sentence'] = s
                # numeric parse best-effort
                if 'value' in p and isinstance(p['value'], str):
                    try:
                        p['value'] = float(p['value'].replace(',','.'))
                    except:
                        pass
                p['confidence'] = p.get('confidence', 0.85)
                results.append(p)
    return results

def parse_json_like(text: str):
    """Best-effort extract JSON array/object from text output."""
    if not text:
        return []
    # try find first JSON bracket
    idx = None
    for ch in ['[','{']:
        i = text.find(ch)
        if i != -1:
            idx = i
            break
    if idx is None:
        return []
    try:
        return json.loads(text[idx:])
    except Exception:
        # fallback: try to sanitize simple arrays like: [{"name":"a","value":"10"}]
        try:
            # remove trailing stuff
            js = text[idx:]
            # drop any text after last closing bracket
            last = max(js.rfind(']'), js.rfind('}'))
            if last != -1:
                js = js[:last+1]
            return json.loads(js)
        except Exception:
            return []


def generate_interpretations_mistral(mistral_gen, texts: List[str]) -> List[str]:
    outs = []
    prompt_base = "Provide a one-sentence human readable interpretation of this KPI (in French). Input: "
    for t in texts[:30]:
        prompt = prompt_base + t
        outs = mistral_gen(prompt, max_new_tokens=80)[0]["generated_text"]
        
    return outs