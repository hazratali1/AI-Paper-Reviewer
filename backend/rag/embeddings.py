"""
Embedding pipeline: converts text chunks into vector embeddings
and stores/loads them in a FAISS index using sentence-transformers.
"""
import os
import json
import pickle
import numpy as np
import faiss
from typing import List, Tuple
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"  # smaller but fast; swap to bge-large for accuracy
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """Embed a list of text strings. Returns float32 numpy array shape (N, D)."""
    model = get_model()
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)
    return embeddings.astype(np.float32)


def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """Build a FAISS inner product index (cosine sim since embeds are normalized)."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index


def save_index(index: faiss.Index, chunks: List[str], save_dir: str) -> None:
    """Save FAISS index and associated chunks to disk."""
    os.makedirs(save_dir, exist_ok=True)
    faiss.write_index(index, os.path.join(save_dir, "index.faiss"))
    with open(os.path.join(save_dir, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)


def load_index(save_dir: str) -> Tuple[faiss.Index, List[str]]:
    """Load FAISS index and chunks from disk."""
    index = faiss.read_index(os.path.join(save_dir, "index.faiss"))
    with open(os.path.join(save_dir, "chunks.pkl"), "rb") as f:
        chunks = pickle.load(f)
    return index, chunks


def create_paper_index(chunks: List[str], save_dir: str) -> Tuple[faiss.Index, List[str]]:
    """Embed chunks, build index, save to disk and return."""
    embeddings = embed_texts(chunks)
    index = build_faiss_index(embeddings)
    save_index(index, chunks, save_dir)
    return index, chunks
