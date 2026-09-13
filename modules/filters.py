# interface/filters.py
import streamlit as st
import pandas as pd

def show_filters():
    st.sidebar.header("Connexions & Configurations")
    st.sidebar.markdown("---")
    gcp_api_key = st.sidebar.text_input( "GCP API Key", type="password", help="Vertex AI doit être activé pour certains modules vision")

    mistral_api_key = st.sidebar.text_input( "Mistral API Key", type="password")

    openai_api_key = st.sidebar.text_input( "OpenAI API Key", type="password")

    return {        
        "gcp_api_key": gcp_api_key,   
        "mistral_api_key": mistral_api_key,
        "openai_api_key": openai_api_key     
    }
