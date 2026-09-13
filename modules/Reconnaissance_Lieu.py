import streamlit as st
from modules.filters import show_filters
from PIL import Image, ImageDraw
import numpy as np


if 'page' not in st.session_state:
    st.session_state.page = 'page1'

def resize_image(image):
    width, height = image.size
    resized_image = image.resize((width//2, height//2), Image.LANCZOS)
    return resized_image

# Ajouter un halo de couleur à l'image
def add_halo(image, color):
    # Créer une nouvelle image avec un halo de couleur
	width, height = image.size

	# Taille du halo (plus petit que l'image)
	halo_margin = 30
	halo = Image.new('RGBA', (width, height), (0, 0, 0, 0))
	halo_draw = ImageDraw.Draw(halo)
	halo_draw.ellipse(
	    (halo_margin, halo_margin, width - halo_margin, height - halo_margin),
	    fill=color,
	    outline=color
	)

	# Coller l'image originale au centre du halo
	image_with_halo = Image.new('RGBA', (width, height))
	image_with_halo.paste(halo, (0, 0), halo)
	image_with_halo.paste(image, (0, 0), image)
	return image_with_halo


def display_dashboard(image):
	
	st.set_page_config(layout="wide")
	st.title("Namsan Tower avec Halo de Lumière")
	col1, col2 = st.columns([2,1])
	with col1:
		if 'current_image' not in st.session_state:
			st.session_state.current_image = resize_image(image)
		st.image(st.session_state.current_image, use_container_width =False)
	with col2:
		color_options = {
			'Vert': (0, 255, 0, 128),
			'Bleu': (0, 0, 255, 128),
			'Orange': (255, 165, 0, 128),
			'Rouge': (255, 0, 0, 128),
			'Violet': (128, 0, 128, 128)
			}
		color_choice = st.selectbox('Choisissez une couleur pour le halo', list(color_options.keys()))
		if st.button('Appliquer le halo'):
			resized_image = resize_image(image)
		st.session_state.current_image = add_halo(resized_image, color_options[color_choice])
		