# app_kpi_universal_mistral.py
"""
Pipeline KPI universel (multidomain) - Streamlit
LLM backend: Mistral via Hugging Face transformers (optionnel)
Features:
- Import TXT / PDF (pdfplumber / OCR fallback)
- Regex candidate extraction
- Optional LLM structuring using Mistral (HF pipeline)
- Embeddings-based classification (sentence-transformers)
- Normalization, scoring, context linking
- Table affichée avec interprétation + graphiques adaptés
"""

import streamlit as st
from pathlib import Path
from utils.pipelines import run_pipeline_kpi
from utils.file_utils import parse_uploaded_file
from utils.display_utils import smart_display


CONFIG = st.session_state.CONFIG

st.set_page_config(page_title="KPI Extractor — Universal (Mistral)", layout="wide")

# ------------------------------
# CONFIGURATION
# ------------------------------
DEFAULT_CONFIG = {
    "llm_enabled": False,
    "llm_backend": "mistral",  # only 'mistral' implemented in this script
    "mistral_model": "mistralai/mistral-1-7b-instruct",  # example; adjust if not available
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "display_context_chars": 220,
    "min_confidence": 0.45
}


# ------------------------------
# STREAMLIT UI
# ------------------------------
def run():
    if st.button("⬅️ Retour au catalogue"):
        del st.session_state['current_page']
        st.rerun()  # reviens sur le main
          
    st.title("Extraction KPI")
    st.markdown("Pipeline multi-domaine : OCR/Parsing → Regex → LLM (Mistral) → Embeddings → Normalisation → Scoring → Dashboard")

    # Sidebar config
    with st.expander("Configuration"):
        st.checkbox("Activer Mistral LLM (Hugging Face)", key="llm_toggle", value= False)
        if st.session_state.llm_toggle:
            st.text_input("Mistral HF model name", key="mistral_model", value="mistralai/mistral-1-7b-instruct")
            st.write("⚠️ Assure-toi d'avoir accès au modèle Hugging Face (token) si nécessaire.")
        st.slider("Contexte affiché (chars)", 100, 800, key="ctx_chars", value=220)

    st.markdown("### 1) Charger un document (TXT ou PDF)")
    uploaded = st.file_uploader("Utilise le rapport exemple ou Importe un .txt ou .pdf", type=["txt","pdf"])
    raw_text = ""
    if st.button("Charger exemple rapport Smart city 2024"):
          sample = Path("data\docs\Rapport_SmartCity_Paris_2024.txt")
          if sample.exists():
                  raw_text = sample.read_text(encoding="utf-8")
                  st.success("Rapport chargé")
	
    if uploaded:
        raw_text = parse_uploaded_file(uploaded)

    if not raw_text or raw_text.strip()=="":
        st.info("Import un fichier, puis clique sur 'Extraire KPI'.")
        st.stop()

    if st.button("Extraire KPI"):
        with st.spinner("Exécution pipeline..."):
            df = run_pipeline_kpi(raw_text)
            st.session_state["kpi_df"] = df
            st.success(f"Extraction terminée — {len(df)} KPI candidats trouvés.")

    if "kpi_df" in st.session_state:
        smart_display(st.session_state["kpi_df"])
        st.markdown("---")
        if st.button("Exporter JSON"):
               js = st.session_state["kpi_df"].to_json(orient="records", force_ascii=False)
               st.download_button("Télécharger JSON", js, "kpi_extracted.json", "application/json")
