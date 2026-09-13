## App.py
import streamlit as st
import pandas as pd
from modules.page1 import display_dashboard
from pathlib import Path
from PIL import Image, ImageDraw

# 
@st.cache_data

def load_image():
	img_path = Path(__file__).parent / "data" / "images" / "namsantower.png"
	image = Image.open(img_path)
	return image

def main():
    image = load_image()
    display_dashboard(image)

if __name__ == "__main__":
    main()
