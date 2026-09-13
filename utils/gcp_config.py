import streamlit as st

def get_gcp_key(api_key):
    return st.secrets.get("GCP_API_KEY", api_key)
