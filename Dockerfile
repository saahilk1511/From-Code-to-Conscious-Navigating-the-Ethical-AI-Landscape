# Shared base
FROM python:3.10-slim AS base
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Backend image
FROM base AS backend
COPY backend/ ./backend/
WORKDIR /app/backend
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]

# Frontend image
FROM base AS frontend
COPY frontend/ ./frontend/
WORKDIR /app/frontend
ENV PORT=8501
EXPOSE 8501
CMD ["streamlit","run","app.py","--server.port=8501","--server.address=0.0.0.0"]