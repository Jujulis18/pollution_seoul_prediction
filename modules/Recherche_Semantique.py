import streamlit as st
from utils.pipelines import semantic_search_pipeline

CONFIG = st.session_state.CONFIG

def run():

	# Bouton de retour
	if st.button("⬅️ Retour au catalogue"):
		del st.session_state['current_page']
		st.rerun()  # reviens sur le main

	with st.expander("⚙️ Paramètres de la pipeline", expanded=False):
		config1, config2 = st.columns(2)
		with config1:
			st.subheader("**Indexation**")
			CONFIG["pipeline_type"] = st.selectbox(
				"Pipeline type",
				options=["A", "B"],
				help='"A" = chunk avant embed, "B" = embed doc complet',
				index=0 if CONFIG["pipeline_type"] == "A" else 1
			)
		
			CONFIG["chunk_method"] = st.selectbox(
				"Chunk method",
				options=["sentence", "paragraph", "sliding"],
				help="Méthode de découpage des textes",
				index=["sentence", "paragraph", "sliding"].index(CONFIG["chunk_method"])
			)
		
			CONFIG["chunk_size"] = st.number_input(
				"Chunk size",
				min_value=50, max_value=5000, step=50,
				value=CONFIG["chunk_size"],
				help="Taille maximale de chaque chunk"
			)
			
			CONFIG["chunk_overlap"] = st.number_input(
				"Chunk overlap",
				min_value=0, max_value=500, step=10,
				value=CONFIG["chunk_overlap"],
				help='Nombre de caractères en chevauchement pour "sliding"'
			)
			
			CONFIG["embedding_model"] = st.text_input(
				"Embedding model",
				value=CONFIG["embedding_model"],
				help="Modèle SentenceTransformers utilisé pour les embeddings"
			)
			
			CONFIG["reduce_dim"] = st.checkbox(
				"Réduire la dimension des embeddings",
				value=CONFIG["reduce_dim"]
			)
			
			if CONFIG["reduce_dim"]:
				CONFIG["reduced_dim"] = st.number_input(
					"Dimension réduite",
					min_value=32, max_value=1024, step=32,
					value=CONFIG["reduced_dim"]
				)
			
			
		with config2:
			st.subheader("**Generation response**")
			CONFIG["index_type"] = st.selectbox(
				"Index type",
				options=["faiss", "annoy"],
				index=0 if CONFIG["index_type"] == "faiss" else 1
			)

			CONFIG["ranking"] = st.checkbox(
				"Activer le reranking",
				value=CONFIG["ranking"]
			)
		
			if CONFIG["ranking"]:
				CONFIG["rerank_model"] = st.text_input(
					"Rerank model",
					value=CONFIG["rerank_model"]
				)
			
			CONFIG["llm_reformulation"] = st.checkbox(
				"Activer la reformulation LLM",
				value=CONFIG["llm_reformulation"]
			)

			if CONFIG["llm_reformulation"]:
				CONFIG["reformulation_model"] = st.selectbox(
					"Reformulation model",
					options=["BART", "T5"],
					index=0 if CONFIG["reformulation_model"]=="BART" else 1
				)
			
			if st.button("💾 Sauvegarder la configuration"):
				st.session_state.CONFIG = CONFIG
				st.success("Configuration sauvegardée ! ✅")		
							
			
		with st.expander("💡 Learn more about impact", expanded=False):
			# Affichage de l'impact (exemple simplifié)
			st.write("""
			- **Pipeline type** : A → les documents sont chunkés avant embedding ; B → embeddings sur doc complet.
			- **Chunk method / size / overlap** : affecte la granularité et la précision des embeddings.
			- **Embedding model** : influence la qualité et la taille des vecteurs.
			- **Reduce_dim** : réduit la mémoire mais peut perdre de l'information.
			- **Index type** : FAISS rapide et robuste ; Annoy moins précis mais plus léger.
			- **Ranking / rerank_model** : améliore la pertinence mais coûte plus de temps CPU.
			- **Reformulation LLM** : permet de reformuler les questions / requêtes pour plus de précision.
			""")

	

	st.title("Recherche sémantique")

	col1, col2 = st.columns(2)

	with col1:
		st.header("Entrée")
		user_query = st.text_area("Que veux tu savoir ?", height=200, help="Pose une question en lien avec le document exemple sur le makgeolli.")
		uploaded_file = st.file_uploader("Utilise le document exemple ou upload votre propre fichier texte", type=["txt"])
		if uploaded_file:
			document = uploaded_file.read().decode("utf-8")
		else:
			document = """
			Le makgeolli est une boisson traditionnelle coréenne légèrement alcoolisée à base de riz.
			Il existe différentes variétés selon la région et la méthode de fermentation.
			Sa texture est laiteuse, son goût légèrement sucré et acidulé.
			Certains producteurs modernes expérimentent avec des levures spécifiques pour améliorer la stabilité.
			"""

		if st.button("Analyser"):
			if user_query.strip() != "":
				question = user_query
			else:
				question = "Comment est fabriqué le makgeolli ?"
			response, execution_time = semantic_search_pipeline(document, question)

			# Stocker résultat pour affichage
			st.session_state['response'] = response
			st.session_state['execution_time'] = execution_time

	with col2:
		st.header("Résultat")
		if 'response' in st.session_state:
			st.subheader("Response")
			st.write(st.session_state['response'])
		if 'execution_time' in st.session_state:
			st.subheader("Temps d'exécution")
			st.write(f"Temps d'indexation : {st.session_state['execution_time'][0]:.3f} secondes\n Temps d'exécution : {st.session_state['execution_time'][1]} secondes")