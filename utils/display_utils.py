
import streamlit as st
import pandas as pd
from utils.llm_utils import generate_interpretations_mistral

# ------------------------------
# DISPLAY helpers
# ------------------------------
def smart_display(df: pd.DataFrame):
    st.subheader("Table des KPI extraits (explicative)")
    if df.empty:
        st.info("Aucun KPI détecté.")
        return
    df_disp = df.copy()
    df_disp["sentence_snip"] = df_disp["sentence"].apply(lambda s: (s[:220] + "...") if len(s)>220 else s)
    # Add interpretation column (simple heuristics or LLM)
    if False and "mistral_gen" in st.session_state and st.session_state.mistral_gen is not None:
    #if st.session_state.KPI_CONF["llm_enabled"] and "mistral_gen" in st.session_state and st.session_state.mistral_gen is not None:
        # ask LLM to produce a one-line interpretation per KPI (best-effort)
        to_interpret = df_disp.apply(lambda r: f"{r.kpi_name} = {r.raw_value} ({r.unit}) ; context: {r.sentence_snip}", axis=1).tolist()
        interp = generate_interpretations_mistral(st.session_state.mistral_gen, to_interpret)
        df_disp["interpretation"] = interp + [""]*(len(df_disp)-len(interp))
    else:
        df_disp["interpretation"] = df_disp.apply(lambda r: f"{r.kpi_name} : valeur {r.raw_value} {r.unit or ''}. Trend={r.trend}", axis=1)
    # nice column order
    cols = ["kpi_name","category","raw_value","value","unit","trend","confidence","sentence_snip","interpretation"]
    st.dataframe(df_disp[cols].rename(columns={
        "kpi_name":"KPI",
        "raw_value":"Valeur brute",
        "sentence_snip":"Contexte (extrait)",
        "interpretation":"Interprétation (one-line)"
    }), use_container_width=True)
    
