import streamlit as st
from utils.nlp_basic import classify_and_generate_email


CONFIG = st.session_state.CONFIG

def run():

	# Bouton de retour
	if st.button("⬅️ Retour au catalogue"):
		del st.session_state['current_page']
		st.rerun()  # reviens sur le main

	st.title("Classification & Email")
	col1, col2 = st.columns(2)

	with col1:
		st.header("Entrée")
		# Choix données de démo ou upload
		demo_data = ["""
						Bonjour,
						Je suis très déçue de votre service client. 
						J’ai signalé un problème il y a une semaine et personne ne m’a répondu. 
						J’aimerais que ce soit réglé rapidement.
						Cordialement,
						Julie
					""", 
					"""Bonjour,
						Je n’arrive pas à me connecter à mon compte depuis hier, l’application affiche une erreur de serveur.  
						Pouvez-vous me dire quand le service sera de nouveau disponible ?
						Merci,
						Alexandre
						""", 
					"""Bonjour,
						Merci pour votre nouvelle interface, elle est vraiment plus claire !  
						Petite question : est-ce qu’il est possible d’exporter mes données en CSV ?
						Bonne journée,
						Sophie
						"""]
		option = st.selectbox("Choisir un email de test :", demo_data)
		uploaded_file = st.file_uploader("Ou upload votre propre fichier texte", type=["txt"])

		if uploaded_file:
			text_input = uploaded_file.read().decode("utf-8")
		else:
			text_input = option

		if st.button("Analyser"):
			# Appel à la fonction métier
			category, email_response = classify_and_generate_email(text_input)

			# Stocker résultat pour affichage
			st.session_state['category'] = category
			st.session_state['response'] = email_response

	with col2:
		st.header("Résultat")
		if 'category' in st.session_state:
			st.subheader("Catégorie détectée")
			st.write(st.session_state['category'])
			st.subheader("Email généré")
			st.write(st.session_state['response'])