# 🧭 AI Risk Navigator

**AI Risk Navigator** is a Retrieval-Augmented Generation (RAG) chatbot that enables contextual Q&A over internal risk, compliance, and policy PDFs. Powered by OpenAI's GPT models, SentenceTransformers, ChromaDB, FastAPI, and Streamlit, it provides explainable, source-grounded answers for high-stakes domains.

This project is featured in the book _Artificial Intelligence and Safety: A Practical Guide for Programmers and Decision Makers_, and demonstrates how LLMs can be ethically leveraged to assist in AI-powered risk management.

---

## 📑 Table of Contents

- [Demo](#demo)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [Challenges & Next Steps](#challenges--next-steps)

---

## 🚀 Demo

<p align="center">
  <img width="1913" height="442" alt="Figure 60" src="https://github.com/user-attachments/assets/53325ba4-8d9c-492c-a672-959ab88fe16b" />
  <img width="1918" height="508" alt="Figure 61" src="https://github.com/user-attachments/assets/49f6915e-4d2e-467f-a6fa-ba16648da76b" />
  <img width="1795" height="886" alt="Figure 62" src="https://github.com/user-attachments/assets/70acb0bb-76a1-4810-b87c-00f6a7ae9118" />
  <img width="1794" height="318" alt="Figure 63" src="https://github.com/user-attachments/assets/c7c26110-432f-4954-b7f4-74f2a9c06c7f" />
</p>

- Ask risk-related questions like:
  > “What are the GDPR retention rules for transaction data?”
- View real-time responses with inline citations.
- Explore source documents directly via the UI.

---

## 🧠 Architecture Overview

**AI Risk Navigator** is composed of 5 core modules:

1. **PDF Processor**  
   Extracts, chunks, and tokenizes long policy or regulatory documents.

2. **Embedder**  
   Converts chunks into semantic vectors using `all-MiniLM-L6-v2`.

3. **Vector Store (ChromaDB)**  
   Stores and retrieves top-k document chunks relevant to user queries.

4. **LLM Generator**  
   Constructs a contextual prompt from retrieved chunks and generates a grounded response using OpenAI’s GPT (`o1-mini`, `gpt-3.5-turbo`, etc.).

5. **Frontend (Streamlit)**  
   Displays the chat interface, conversation history, and document sources.

---

## 📁 Project Structure

```
AI-Risk-Navigator/
├── backend/
│   ├── main.py                  # FastAPI endpoint (/chat)
│   ├── document_processor.py    # PDF loading, chunking
│   ├── chroma_manager.py        # Vector DB interface
├── frontend/
│   └── app.py                   # Streamlit UI
├── data/                        # PDF transcripts or policy docs
├── chroma_db/                   # Persisted vector database
├── .env                         # API keys and paths
├── Dockerfile                   # Image config
├── docker-compose.yml           # Multi-container setup
└── requirements.txt             # Python dependencies
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/AI-Risk-Navigator.git
cd AI-Risk-Navigator
```

2. **Create a `.env` file**

```env
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=o1-mini
DOCS_PATH=/app/data
CHROMA_DIR=/app/chroma_db
API_URL=http://backend:8000/chat
```

3. **Add your documents**

Place your PDF files in the `./data/` directory.

---

## ▶️ Running the Project

Make sure you have Docker installed, then run:

```bash
docker-compose up --build
```

Once both services have started to access the chatbot, open :

- **Chatbot interface:** [http://localhost:8501](http://localhost:8501)  
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

To stop the application, press Ctrl+C. To stop and remove its containers, run:

```bash
docker-compose down
```
---

## 💬 Usage

1. Enter your question in the input box (e.g., _"What’s the retention policy for financial records?"_).
2. The chatbot retrieves relevant chunks from the indexed PDFs.
3. GPT generates a response using the retrieved context.
4. Expand **Sources Used** to view citation metadata.

---

## ⚠️ Challenges & Next Steps

- Improve chunking strategy to better preserve semantic boundaries
- Add real-time document upload and re-indexing
- Optimize latency with asynchronous embedding + retrieval
- Extend to multimodal documents (e.g., scanned PDFs with OCR)
- Introduce user access control and audit logging

---

> Built as part of *From Code to Conscious: Navigating the Ethical AI Landscape* — demonstrating ethical, explainable AI in high-risk domains.
