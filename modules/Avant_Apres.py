import streamlit as st
from utils.vision_tools import compare_images

def run():
	
    # Bouton de retour
	if st.button("⬅️ Retour au catalogue"):
		del st.session_state['current_page']
		st.rerun()  # reviens sur le main

	st.title("🖼️ Comparaison Avant / Après")

	img1 = st.file_uploader("Image AVANT", type=["jpg", "png"])
	img2 = st.file_uploader("Image APRÈS", type=["jpg", "png"])

	if st.button("Comparer"):
		if img1 and img2:
			diff, list = compare_images(img1, img2)
			if diff:
				st.markdown(f"Changements détectés : {list}")
			else:
				st.markdown(list)
		else:
			st.warning("Merci d’uploader deux images.")
		