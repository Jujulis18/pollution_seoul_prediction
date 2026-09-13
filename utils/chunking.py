import numpy as np
import faiss
from sentence_transformers import CrossEncoder, SentenceTransformer
from sklearn.decomposition import PCA
from transformers import pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st

from sklearn.metrics.pairwise import cosine_similarity
import nltk


CONFIG = st.session_state.CONFIG

# --- Étape 1 : Chunking ---
def chunk_document(text, method=CONFIG["chunk_method"], size=CONFIG["chunk_size"], overlap=CONFIG["chunk_overlap"]):
    if method == "sentence":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            separators=[".", "!", "?"],
        )
        chunks = splitter.split_text(text)
    elif method == "paragraph":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n"],
        )
        chunks = splitter.split_text(text)
    elif method == "sliding":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
            separators=[".", "!", "?", "\n", " "],
        )
        chunks = splitter.split_text(text)
    else:
        raise ValueError("Méthode de chunking non reconnue.")

    return [c.strip() for c in chunks if len(c.strip()) > 0]

     

# --- Étape 2 : Embedding ---
def get_embeddings(chunks, model_name=CONFIG["embedding_model"]):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks)
    return np.array(embeddings)

# =============================
# RÉDUCTION DE DIMENSION
# =============================

def reduce_embeddings(embeddings, target_dim):
    """Réduction PCA optionnelle."""
    pca = PCA(n_components=target_dim)
    reduced = pca.fit_transform(embeddings)
    return reduced

# --- Étape 3 : Indexation FAISS ---
def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    if CONFIG["index_type"] == "flatL2":
        index = faiss.IndexFlatL2(dim)
    else:
        index = faiss.IndexHNSWFlat(dim, 32)  # Example for HNSW
    
    index.add(embeddings)
    return index


# --- Étape 4 : Recherche ---
def search_query(index, query, model_name=CONFIG["embedding_model"], k=3):
    model = SentenceTransformer(model_name)
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, k)
    return distances, indices


# --- Étape 5 : (optionnel) Ranking ---
def rerank_results(chunks, query, model_name=CONFIG["rerank_model"]):
    """Reclasse les résultats avec un modèle de reranking."""
    if not CONFIG["ranking"]:
        return chunks
    cross_encoder = CrossEncoder(model_name)
    pairs = [[query, c] for c in chunks]
    scores = cross_encoder.predict(pairs)
    ranked = [chunk for _, chunk in sorted(zip(scores, chunks), reverse=True)]
    return ranked


# --- Étape 6 : (optionnel) Réécriture LLM ---
def reformulate_answer(chunks, query, model_name=CONFIG["reformulation_model"]):
    """
    Reformule ou synthétise la réponse à partir des chunks pertinents,
    en utilisant un modèle Hugging Face (BART ou T5).
    """
    if not CONFIG["llm_reformulation"]:
        return " ".join(chunks[:2])

    # Combine les chunks sélectionnés
    combined_text = " ".join(chunks[:3])
    prompt = f"Question : {query}\nTexte : {combined_text}\nRéponse synthétique :"
    
    # Sélection du modèle
    if model_name.upper() == "BART":
        summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            truncation=True,
        )
    elif model_name.upper() == "T5":
        summarizer = pipeline(
            "text2text-generation",
            model="t5-base",
            truncation=True,
        )
    else:
        raise ValueError("Modèle non reconnu. Choisis 'BART' ou 'T5'.")

    # Reformulation
    if model_name.upper() == "BART":
        summary = summarizer(combined_text, max_length=130, min_length=30, do_sample=False)
        return f"🧠 Synthèse ({model_name}) : {summary[0]['summary_text']}"
    else:
        input_text = f"summarize: {prompt}"
        result = summarizer(input_text, max_length=130, min_length=30, do_sample=False)
        return f"🧠 Reformulation ({model_name}) : {result[0]['generated_text']}"

def semantic_segment(text, threshold=0.6):
    """
    Découpe une transcription en segments thématiques selon la similarité sémantique.
    Utilise les embeddings de phrases successives et coupe quand la similarité baisse trop.
    """
    

    # Découpage en phrases
    sentences = nltk.sent_tokenize(text)
    if len(sentences) < 2:
        return [{"topic_id": 0, "text": text}]
    st.markdown(f"- 🪓 {len(sentences)} phrases identifiées pour segmentation.")
    # Embeddings des phrases
    sentence_embeddings = get_embeddings(sentences)

    segments = []
    current_segment = [sentences[0]]
    current_topic_id = 0
    st.markdown(f"- 🪓 Démarrage du segment {current_topic_id}.")
    for i in range(1, len(sentences)):
        sim = cosine_similarity(
            [sentence_embeddings[i - 1]], [sentence_embeddings[i]]
        )[0][0]

        if sim < threshold:
            # Nouvelle section
            segments.append({
                "topic_id": current_topic_id,
                "text": " ".join(current_segment)
            })
            current_segment = [sentences[i]]
            current_topic_id += 1
        else:
            current_segment.append(sentences[i])

    # Dernier segment
    segments.append({
        "topic_id": current_topic_id,
        "text": " ".join(current_segment)
    })
    st.markdown(f"- 🪓 Segment {current_topic_id} final ajouté.")
    return segments
