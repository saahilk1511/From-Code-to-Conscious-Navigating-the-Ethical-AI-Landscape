import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Local imports (no `backend.` prefix)
from document_processor import DocumentProcessor
from chroma_manager import ChromaDBManager

# Load .env
load_dotenv(dotenv_path=".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DOCS_PATH      = os.getenv("DOCS_PATH", "/app/data")
CHROMA_DIR     = os.getenv("CHROMA_DIR", "/app/chroma_db")
API_MODEL      = os.getenv("OPENAI_MODEL", "o4-mini-2025-04-16")

# Initialize the new v1 client
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# Build & index at startup
processor   = DocumentProcessor(DOCS_PATH)
chunks      = processor.get_chunks()
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma      = ChromaDBManager(CHROMA_DIR)
chroma.index(chunks, embed_model.encode)

class ChatRequest(BaseModel):
    messages: list[dict]

class ChatResponse(BaseModel):
    response: str
    sources:  list[dict]

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.messages:
        raise HTTPException(400, "Empty message list")

    # 1) Embed + retrieve
    user_q = req.messages[-1]["content"]
    q_emb  = embed_model.encode([user_q])[0]
    hits   = chroma.query(q_emb, top_k=5)

    # 2) Build prompt
    #context = "\n---\n".join([h["text"] for h in hits])
    #system_msg = {
     #   "role": "system",
      #  "content": f"You are an assistant. Use the following context to answer the question:\n{context}"
    #}
    #msgs = [system_msg] + req.messages

    # 2) Fold the system prompt into a user message
    context = "\n---\n".join(h["text"] for h in hits)
    prompt_with_context = (
        "You are an assistant. Use the following context to answer the question:\n"
        f"{context}"
    )
    # NOTE: role is now "user" so o1-mini will accept it
    instruction_msg = {"role": "user", "content": prompt_with_context}

    msgs = [instruction_msg] + req.messages

    # 3) Call OpenAI v1
    resp = client.chat.completions.create(
        model=API_MODEL,
        messages=msgs
    )

    # 4) Return
    answer = resp.choices[0].message.content
    return ChatResponse(response=answer, sources=hits)
