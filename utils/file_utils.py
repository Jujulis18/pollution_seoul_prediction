import streamlit as st

# ------------------------------
# UTIL: parse uploaded file (txt/pdf) with OCR fallback
# ------------------------------
# Optional heavy libs
try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    from PIL import Image
    import pytesseract
    from pdf2image import convert_from_bytes
except Exception:
    pytesseract = None
    convert_from_bytes = None

# Transformers (for Mistral)
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
except Exception:
    pipeline = None

# Embeddings
try:
    from sentence_transformers import SentenceTransformer, util
except Exception:
    SentenceTransformer = None
    util = None


def parse_uploaded_file(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    name = uploaded_file.name.lower()
    raw = uploaded_file.read()
    if name.endswith(".txt"):
        try:
            return raw.decode("utf-8")
        except:
            return raw.decode("latin-1", errors="ignore")
    elif name.endswith(".pdf"):
        # try pdfplumber
        if pdfplumber:
            try:
                with pdfplumber.open(uploaded_file) as pdf:
                    pages = [p.extract_text() or "" for p in pdf.pages]
                return "\n".join(pages)
            except Exception:
                pass
        # fallback OCR if tools available
        if convert_from_bytes and pytesseract:
            try:
                images = convert_from_bytes(raw)
                texts = [pytesseract.image_to_string(img, lang='fra') for img in images]
                return "\n".join(texts)
            except Exception:
                pass
        st.warning("Impossible d'extraire le texte du PDF (installez pdfplumber ou pytesseract+pdf2image).")
        return ""
    else:
        st.error("Format non supporté. Utilise .txt ou .pdf")
        return ""