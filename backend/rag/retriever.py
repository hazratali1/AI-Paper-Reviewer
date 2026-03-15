"""
RAG Retriever: Top-K similarity search over a FAISS index.
Returns the most relevant text chunks for a given query.
"""
import numpy as np
import faiss
from typing import List
from rag.embeddings import embed_texts, load_index


def retrieve(query: str, index: faiss.Index, chunks: List[str], top_k: int = 5) -> List[str]:
    """
    Retrieve top_k most similar chunks for the given query.
    """
    query_embedding = embed_texts([query])  # shape (1, D)
    scores, indices = index.search(query_embedding, top_k)
    results = []
    for idx in indices[0]:
        if 0 <= idx < len(chunks):
            results.append(chunks[idx])
    return results


def retrieve_from_disk(query: str, save_dir: str, top_k: int = 5) -> List[str]:
    """Convenience: load index from disk, then retrieve."""
    index, chunks = load_index(save_dir)
    return retrieve(query, index, chunks, top_k=top_k)


def build_context(chunks: List[str], max_tokens: int = 3000) -> str:
    """Join retrieved chunks into a single context string, respecting a rough token limit."""
    context = ""
    for chunk in chunks:
        if len(context.split()) + len(chunk.split()) > max_tokens:
            break
        context += chunk + "\n\n"
    return context.strip()
