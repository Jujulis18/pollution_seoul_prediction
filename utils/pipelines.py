import time
import streamlit as st
import pandas as pd
from utils.regex_utils import regex_extract_candidates, normalize_candidate
from utils.llm_utils import load_mistral_pipeline, llm_structured_extraction
from utils.chunking import chunk_document, get_embeddings, reduce_embeddings, build_faiss_index, search_query, rerank_results, reformulate_answer, semantic_segment
from utils.embeddings_utils import merge_and_score



CONFIG = st.session_state.CONFIG
# =============================
# Pipelines
# =============================

def pipeline_A(text, query):
    """Flow A: chunk → embed → FAISS → query"""
    t1 = time.perf_counter()
    chunks = chunk_document(text)
    embeddings = get_embeddings(chunks, CONFIG["embedding_model"])
    if CONFIG["reduce_dim"]:
        embeddings = reduce_embeddings(embeddings, CONFIG["reduced_dim"])
    index = build_faiss_index(embeddings)
    t2 = time.perf_counter()
    _, idx = search_query(index, query, CONFIG["embedding_model"])
    results = [chunks[i] for i in idx[0]]
    results = rerank_results(results, query, CONFIG["rerank_model"])
    answer = reformulate_answer(results, query, CONFIG["reformulation_model"])
    t3 = time.perf_counter()
    return answer, compute_execution_time(t1, t2, t3)

def pipeline_B(text, query):
    """Flow B: embed full doc → FAISS → query → retrieve chunk → reformulate"""
    t1 = time.perf_counter()
    # Étape 1 : embed le document complet
    embeddings = get_embeddings([text], CONFIG["embedding_model"])
    if CONFIG["reduce_dim"]:
        embeddings = reduce_embeddings(embeddings, CONFIG["reduced_dim"])
    index = build_faiss_index(embeddings)
    t2 = time.perf_counter()
    # Étape 2 : recherche sémantique
    _, idx = search_query(index, query, CONFIG["embedding_model"])
    
    # Étape 3 : récupération des chunks pertinents
    chunks = chunk_document(text, CONFIG["chunk_size"])
    results = [chunks[i % len(chunks)] for i in idx[0]]  # simple mapping
    results = rerank_results(results, query, CONFIG["rerank_model"])
    answer = reformulate_answer(results, query, CONFIG["reformulation_model"])
    t3 = time.perf_counter()
    return answer, compute_execution_time(t1, t2, t3)

# =============================
# Pipeline principal
# =============================

def semantic_search_pipeline(text, query):
    if CONFIG["pipeline_type"] == "A":
        return pipeline_A(text, query)
    else:
        return pipeline_B(text, query)
    

# =============================
# Metrics (à développer)
# =============================

def compute_execution_time(t1, t2, t3):
    # base emebddings time (chunk, enmbedding, index)
    preprocessing_time = t2 - t1

    # search time (embed query, search, rerank, reformulate)
    search_time = t3 - t2
    return [preprocessing_time, search_time]



# ------------------------------
# MAIN PIPELINE RUN
# ------------------------------



def run_pipeline_kpi(document_text: str):
    # 1. regex candidates
    candidates = regex_extract_candidates(document_text)
    normed = [normalize_candidate(c) for c in candidates]
    # 2. optionally load mistral pipeline and run structured LLM over unique sentences
    llm_structs = []
    if False:
    #if st.session_state.KPI_CONF["llm_enabled"]:
        # load pipeline once
        if "mistral_gen" not in st.session_state:
            st.session_state.mistral_gen = load_mistral_pipeline(st.session_state.KPI_CONF["mistral_model"])
        mistral_gen = st.session_state.get("mistral_gen")
        if mistral_gen:
            unique_sentences = list({n["sentence"] for n in normed})
            llm_structs = llm_structured_extraction(mistral_gen, unique_sentences, top_k=40)
    # 3. merge & score
    merged = merge_and_score(normed, llm_structs)
    df = pd.DataFrame(merged)
    if not df.empty:
        df = df.sort_values(["confidence","start"], ascending=[False, True]).reset_index(drop=True)
    return df

# =============================
# reunion summary pipeline
def generate_meeting_summary(text):
    """
    Pipeline complet de génération de compte rendu de réunion structuré par sujet.
    """
    st.markdown("### Pipeline de génération de compte rendu de réunion")
    st.markdown(f"{text[:100]}...")  # affiche un extrait du texte
    # Étape 1 : segmentation sémantique
    segments = semantic_segment(text)
    st.markdown(f"- 🪓 {len(segments)} segments thématiques identifiés.")
    structured_summary = []

    for seg in segments:
        seg_text = seg["text"]

        # Résumé synthétique
        summary = llm_structured_extraction(seg_text, task="summary")
        st.markdown(f"- 📝 Sujet {seg['topic_id'] + 1} résumé : {summary}")
        # Extraction des actions (personne, tâche, date)
        actions = llm_structured_extraction(seg_text, task="actions")
        st.markdown(f"- 📅 {len(actions)} actions identifiées.")
        # Décisions
        decisions = llm_structured_extraction(seg_text, task="decisions")
        st.markdown(f"- ✅ {len(decisions)} décisions identifiées.")
        # KPI / données chiffrées
        kpi_raw = regex_extract_candidates(seg_text)
        kpi_clean = llm_structured_extraction(
            {"raw": kpi_raw, "context": seg_text}, task="kpi"
        )
        st.markdown(f"- 📊 {len(kpi_clean)} KPI extraits.")
        structured_summary.append({
            "topic_id": seg["topic_id"],
            "summary": summary,
            "actions": actions,
            "decisions": decisions,
            "kpi": kpi_clean,
        })

    # Synthèse globale
    global_summary = llm_structured_extraction(
        [seg["summary"] for seg in structured_summary],
        task="global_summary"
    )
    st.markdown("### Synthèse globale générée.")
    return {"global_summary": global_summary, "topics": structured_summary}
