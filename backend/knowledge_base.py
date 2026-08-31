import time
from pathlib import Path
from typing import Dict, List, Any

from chromadb.utils import embedding_functions
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document

from .config import (
    CHROMA_DIR,
    SEED_DOCS_DIR,
    KB_DOCS_DIR,
    RAG_CHUNK_SIZE,
    RAG_CHUNK_OVERLAP,
    RAG_DEFAULT_TOP_K,
)


# Local ONNX Embedding Function & Text Splitter
emb_fn = embedding_functions.DefaultEmbeddingFunction()


class LocalEmbeddings:
    def embed_documents(self, texts):
        return emb_fn(texts)

    def embed_query(self, text):
        return emb_fn([text])[0]


splitter = RecursiveCharacterTextSplitter(
    chunk_size=RAG_CHUNK_SIZE,
    chunk_overlap=RAG_CHUNK_OVERLAP,
)

vec_store = Chroma(
    collection_name="kavach_standards",
    embedding_function=LocalEmbeddings(),
    persist_directory=str(CHROMA_DIR),
)

retriever = vec_store.as_retriever(search_kwargs={"k": RAG_DEFAULT_TOP_K})



# Ingest Seed Documents on Startup
def _seed_db():
    if SEED_DOCS_DIR.exists() and len(vec_store.get().get("ids", [])) == 0:
        for p in SEED_DOCS_DIR.glob("*.*"):

            docs = (
                PyPDFLoader(str(p)).load()
                if p.suffix.lower() == ".pdf"
                else TextLoader(str(p), encoding="utf-8").load()
            )
            for d in docs:
                d.metadata["title"] = p.stem.replace("_", " ").title()
                d.metadata["filename"] = p.name
                d.metadata["doc_id"] = f"DOC-{p.stem}"
            vec_store.add_documents(splitter.split_documents(docs))


_seed_db()


# Simple Knowledge Base Interface (< 50 lines)
class LocalRAGKnowledgeBase:
    def ingest_file(self, file_path: str or Path, original_filename: str = None) -> Dict[str, Any]:
        p = Path(file_path)
        name = original_filename or p.name
        doc_id = f"DOC-{int(time.time() * 1000)}"
        docs = (
            PyPDFLoader(str(p)).load()
            if p.suffix.lower() == ".pdf"
            else TextLoader(str(p), encoding="utf-8").load()
        )
        for d in docs:
            d.metadata["doc_id"] = doc_id
            d.metadata["title"] = name
            d.metadata["filename"] = name
        chunks = splitter.split_documents(docs)
        vec_store.add_documents(chunks)
        return {
            "success": True,
            "filename": name,
            "doc_id": doc_id,
            "indexed_chunks": len(chunks),
            "document": {"doc_id": doc_id, "filename": name, "title": name},
        }

    def ingest_text(self, title: str, text: str, category: str = "STANDARDS") -> Dict[str, Any]:
        doc_id = f"DOC-{int(time.time() * 1000)}"
        doc = Document(page_content=text, metadata={"doc_id": doc_id, "title": title, "filename": title})
        chunks = splitter.split_documents([doc])
        vec_store.add_documents(chunks)
        return {
            "success": True,
            "filename": title,
            "doc_id": doc_id,
            "indexed_chunks": len(chunks),
            "document": {"doc_id": doc_id, "title": title},
        }

    def search(self, query: str, top_k: int = RAG_DEFAULT_TOP_K) -> List[Dict[str, Any]]:
        results = vec_store.similarity_search_with_score(query, k=top_k)
        citations = []
        for doc, dist in results:
            # If distance is too high (> 1.72), it is an irrelevant semantic mismatch
            if dist > 1.72:
                continue

            # Convert distance to normalized relevance percentage
            relevance = max(0.5, min(0.99, round(1.0 - (dist / 3.0), 2)))
            citations.append({
                "doc_id": doc.metadata.get("doc_id", "DOC"),
                "title": doc.metadata.get("title", "Standard Document"),
                "filename": doc.metadata.get("filename", "document.txt"),
                "chunk_index": 1,
                "total_chunks": 1,
                "excerpt": doc.page_content[:250] + "...",
                "full_content": doc.page_content,
                "relevance_score": relevance,
                "distance": round(dist, 3)
            })
        return citations


    def list_documents(self) -> List[Dict[str, Any]]:
        metas = vec_store.get(include=["metadatas"]).get("metadatas", [])
        seen = {}
        for m in metas:
            if m.get("doc_id") and m["doc_id"] not in seen:
                seen[m["doc_id"]] = {
                    "doc_id": m["doc_id"],
                    "title": m.get("title", "Document"),
                    "filename": m.get("filename", "document.txt"),
                }
        return list(seen.values())

    def delete_document(self, doc_id: str) -> bool:
        ids = vec_store.get(where={"doc_id": doc_id}).get("ids", [])
        if ids:
            vec_store.delete(ids=ids)
            return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        ids = vec_store.get().get("ids", [])
        return {"total_documents": len(self.list_documents()), "total_chunks": len(ids)}


knowledge_base = LocalRAGKnowledgeBase()
