
DEFAULT_CONFIG = {
    "pipeline_type": "A",
    "chunk_method": "sentence",
    "chunk_size": 300,
    "chunk_overlap": 100,
    "embedding_model": "all-MiniLM-L6-v2",
    "reduce_dim": False,
    "reduced_dim": 128,
    "index_type": "faiss",
    "ranking": True,
    "rerank_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
    "reformulation_model": "BART",
    "llm_reformulation": True,
}

