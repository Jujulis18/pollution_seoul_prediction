## App.py
import importlib
import streamlit as st
from PIL import Image, ImageOps
# from utils.gcp_config import get_gcp_key
from modules.filters import show_filters
from utils.config_pipeline import DEFAULT_CONFIG

# Initialise la config dans la session Streamlit si pas encore fait
if "CONFIG" not in st.session_state:
    st.session_state.CONFIG = DEFAULT_CONFIG.copy()

CONFIG = st.session_state.CONFIG


# --------- DATA ----------
# Définir les catégories et les process
categories = {
    "NLP / Text Processing": [
        {
            "name": "Classification & Email",
            "desc": "Classe et répond automatiquement aux tickets clients",
            "page": "modules/Classification_Email.py",
            "img": "data/assets/cow-girl.png",
            "active": True
        },
        {
            "name": "Recherche intelligente",
            "desc": "Posez une question sur des documents internes et obtenez une réponse contextuelle",
            "page": "modules/Recherche_Semantique.py",
            "img": "data/assets/cow-girl.png",
            "active": True
        },
        {
            "name": "Extraction KPI",
            "desc": "Identifie et met en forme les entités clés d’un document",
            "page": "modules/Extraction_KPI.py",
            "img": "data/assets/cow-girl.png",
            "active": True
        },
        {
            "name": "Analyse sentiment",
            "desc": "Analyse la tonalité des commentaires ou avis",
            "page": "modules/Sentiment.py",
            "img": "data/assets/cow-girl.png",
            "active": False
        },
        {
            "name": "Résumé réunion",
            "desc": "Génère un compte-rendu clair d’une réunion ou d’une note audio",
            "page": "modules/Resume_Reunion.py",
            "img": "data/assets/cow-girl.png",
            "active": True
        },
        {
            "name": "Commentaire intelligent",
            "desc": "Analyse et génère un feedback ou insight basé sur un texte",
            "page": "modules/Commentaire_Intelligent.py",
            "img": "data/assets/cow-girl.png",
            "active": False
        },
    ],
    "Computer Vision": [
        {
            "name": "Avant / Après",
            "desc": "Compare deux images pour détecter les modifications visuelles",
            "page": "modules/Avant_Apres.py",
            "img": "data/assets/cow-girl.png",
            "active": True
        },
        {
            "name": "Zoom Out / Conformité",
            "desc": "Vérifie qu’un zoom out ne révèle pas d’éléments indésirables",
            "page": "modules/Verif_Conformite.py",
            "img": "data/assets/cow-girl.png",
            "active": False
        },
        {
            "name": "Reconnaissance lieu",
            "desc": "Identifie le type d’environnement sur une image",
            "page": "modules/Reconnaissance_Lieu.py",
            "img": "data/assets/cow-girl.png",
            "active": False
        },
        {
            "name": "Détection défauts",
            "desc": "Détecte anomalies ou défauts sur produits ou surfaces",
            "page": "modules/Detection_Defauts.py",
            "img": "data/assets/cow-girl.png",
            "active": False
        },
    ]
}

# --------- APP ----------

def main():

    show_filters()
    st.set_page_config(
        page_title="AI Use Case Catalog",
        page_icon="🤖",
        layout="wide"
    ) 

    # ---- Navigation dynamique ----
    if 'current_page' in st.session_state:
        page_module_name = st.session_state['current_page'].replace(".py", "").replace("/", ".")
        try:
            page_module = importlib.import_module(page_module_name)
            page_module.run()  # Exécute uniquement la page demandée
            return  # <-- très important pour ne pas afficher la suite
        except ModuleNotFoundError:
            st.error(f"Module {page_module_name} introuvable.")
            return

    # ---- Page d’accueil ----
    st.title("🤖 AI Use Case Catalog")
    st.markdown("""
    Bienvenue dans ton **catalogue d'applications IA**.  
    Sélectionne un use case dans le menu à gauche pour explorer des exemples concrets de :
    - 🧠 NLP (texte, résumé, classification, recherche)
    - 👁️ Computer Vision (analyse d'image, comparaison, détection)
    """)

    st.markdown("---")
    st.markdown("💡 *Ce prototype fonctionne en local avec des résultats simulés. "
                "Il sera ensuite connecté à Vertex AI / Gemini / Mistral via API.*")

    # --------- RENDER CATEGORIES ----------
    for category, processes in categories.items():
        st.subheader(category)
        cols = st.columns(3)  # 3 cards per row
        for i, process in enumerate(processes):
            col = cols[i % 3]
            with col:
                if process["active"]:
                    st.image(process["img"],  width = 150, )
                else:
                    image = Image.open(process["img"])
                    gray_image = ImageOps.grayscale(image)
                    st.image(gray_image,  width = 150, )
                st.markdown(f"**{process['name']}**")
                st.caption(process["desc"])
                if st.button("Accéder", key=f"{category}_{process['name']}"):
                    st.markdown(f"Chargement de **{process['page']}**...")
                    st.session_state['current_page'] = process["page"]
                    st.markdown(f"{st.session_state['current_page']}")
                    st.rerun()  # <-- ici on recharge la page

if __name__ == "__main__":
    main()

