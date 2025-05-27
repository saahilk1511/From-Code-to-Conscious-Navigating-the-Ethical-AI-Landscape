import os
from chromadb import Client
from chromadb.config import Settings

class ChromaDBManager:
    def __init__(self, persist_dir: str, collection_name: str = "rag_collection"):
        os.makedirs(persist_dir, exist_ok=True)
        self.client = Client(Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False,
        ))
        self.col = self.client.get_or_create_collection(collection_name)

    def index(self, chunks: list[dict], embed_fn: callable):
        ids = [c["id"] for c in chunks]
        texts = [c["text"] for c in chunks]
        metadatas = [{"doc_id": c["doc_id"], "chunk_id": c["chunk_id"]} for c in chunks]
        embeddings = embed_fn(texts)
        self.col.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        res = self.col.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        hits = []
        for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
            hits.append({"text": doc, **meta})
        return hits