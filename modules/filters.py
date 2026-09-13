# interface/filters.py
import streamlit as st
import pandas as pd

def show_filters(df):
    st.sidebar.header("Filtres")

    # Pays
    pays = df['country_long'].unique().tolist()
    selection_pays = st.sidebar.multiselect(
        "Sélectionnez les pays",
        options=pays,
        default=pays
    )

    # Sexe
    choix_sexe = st.sidebar.radio(
        "Genre des athlètes",
        options=["Tous", "Homme", "Femme"],
        index=0
    )

    # Type de médaille (exemple simplifié)
    choix_medaille = st.sidebar.multiselect(
        "Type de médaille",
        options=["Or", "Argent", "Bronze", "Total"],
        default=["Total"]
    )
       

    return {
        "pays": selection_pays,
        "sexe": choix_sexe,
        "medaille": choix_medaille
    }
