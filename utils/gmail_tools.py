import urllib.parse
import streamlit as st

recipient = "client@example.com"
subject = "Réponse à votre message"
body = """Bonjour,

Merci pour votre message. Nous vous transmettons les informations demandées.

Bien cordialement,
Julie
"""

gmail_url = (
    "https://mail.google.com/mail/?view=cm&fs=1&"
    + f"to={urllib.parse.quote(recipient)}"
    + f"&su={urllib.parse.quote(subject)}"
    + f"&body={urllib.parse.quote(body)}"
)

st.link_button("✉️ Ouvrir le mail prérempli dans Gmail", gmail_url)
