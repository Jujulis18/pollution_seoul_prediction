
import streamlit as st
import re



CONFIG = st.session_state.CONFIG

def classify_and_generate_email(text_input):
    categories = classify_email(text_input)
    responses = []

    for category in categories:
        response = generate_response_for_category(text_input, category)
        responses.append(response)

    final_email = combine_responses(responses)
    return categories, final_email

def classify_email(text):
    categories = ["Plainte", "Demande d'information", "Retour positif", "Technique"]
    detected = []

    text_lower = text.lower()

    if any(word in text_lower for word in ["problème", "mécontent", "pas satisfait", "erreur"]):
        detected.append("Plainte")

    if any(word in text_lower for word in ["comment", "pouvez-vous", "info", "renseignement", "quand", "où"]):
        detected.append("Demande d'information")

    if any(word in text_lower for word in ["merci", "super", "parfait", "satisfait", "ravie"]):
        detected.append("Retour positif")

    if any(word in text_lower for word in ["bug", "technique", "serveur", "connexion", "crash"]):
        detected.append("Technique")

    return detected

def classify_email_using_llm(text):
    None

# Add a priorité (plainte> technique>demande>positif) 
def generate_response_for_category(text, category):
    if category == "Plainte":
        return (
            "Nous sommes désolés d’apprendre que vous avez rencontré un problème. "
            "Notre équipe va examiner la situation au plus vite afin de corriger cela."
        )

    elif category == "Demande d'information":
        return (
            "Merci pour votre message. Nous vous transmettons les informations demandées "
            "dans les plus brefs délais."
        )

    elif category == "Retour positif":
        return (
            "Merci beaucoup pour vos retours positifs ! "
            "Nous sommes ravis que notre service vous apporte satisfaction."
        )

    elif category == "Technique":
        return (
            "Votre message a bien été transmis à notre équipe technique. "
            "Nous reviendrons vers vous dès que le problème sera résolu."
        )

    else:
        return "Merci pour votre message."

def generate_response_for_category_using_llm(text, category):
    None

def combine_responses(responses):
    if not responses:
        return "Merci pour votre message, nous restons à votre écoute."
    elif len(responses) == 1:
        return responses[0]
    else:
        return " ".join(responses)

# personalisé avec premon, ton formé/amical 
def final_response_using_llm(response):
    None

## Extract KPI
def extract_sentence(text: str, idx: int, window: int = 250) -> str:
    start = max(0, text.rfind('.', 0, idx) + 1)
    end = text.find('.', idx)
    if end == -1:
        end = min(len(text), idx + window)
    return text[start:end].strip()

def parse_number(s: str) -> float:
    if s is None:
        return None
    s = str(s).strip()
    # remove narrow no-break spaces
    s = s.replace('\u202f','').replace('\xa0','')
    # handle spaces as thousands sep
    s = s.replace(' ', '').replace(',', '.')
    # remove trailing letters
    s = re.sub(r'[^\d\.\-]', '', s)
    try:
        return float(s)
    except:
        return None

def infer_trend_from_sentence(sentence: str) -> str:
    s = sentence.lower()
    if any(w in s for w in ["augment", "hausse", "en hausse", "en progression", "progression", "croissance"]):
        return "up"
    if any(w in s for w in ["baisse", "dimin", "en baisse", "réduit", "réduction", "diminution"]):
        return "down"
    # detect "vs" previous year patterns with numbers
    if re.search(r'(\bvs\b|\bcontre\b|\bpar rapport\b)', s):
        return "compared"
    return "unknown"

def infer_kpi_name_from_snippet(snippet: str) -> str:
    s = snippet.lower()
    if any(w in s for w in ["satisfaction","satisfait","satisfaisant"]):
        return "Taux de satisfaction"
    if any(w in s for w in ["infection","nosocomiale","e.i.g"]):
        return "Taux d'infection nosocomiale"
    if any(w in s for w in ["consommation","kwh","gwh","énergie"]):
        return "Consommation d'énergie"
    if any(w in s for w in ["émission","co2","co₂"]):
        return "Émissions de CO2"
    if any(w in s for w in ["hospitalisation","hospitalisations","séjour"]):
        return "Nombre d'hospitalisations"
    return "Indicateur"
