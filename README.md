# RAG Assistant

A REST API service that answers questions based on the project's internal documentation.  
Uses the **RAG (Retrieval-Augmented Generation)** pattern: documents are indexed into FAISS, a query is converted into a vector, relevant chunks are retrieved, and the answer is generated via GPT.

## Stack

- **Django 5 + DRF** — API
- **LangChain** — chain orchestration
- **OpenAI** — embeddings (`text-embedding-3-small`) + LLM (`gpt-4.1-mini`)
- **FAISS** — local vector store

## Structure

```
docs/               # Markdown documentation (knowledge source)
rag_assistant/
  views.py          # POST /api/assistant/
  services/
    qa_service.py   # Business logic: search + answer generation
    embedding.py    # Document indexing
  management/commands/
    load_docs.py    # Django command to build the index
  constants/
    constants.py    # Paths, models, parameters
  faiss_index/      # Saved FAISS index
```

## Running

```bash
# Start
docker-compose up --build

# Index documentation (once or after updating docs/)
docker exec django_rag python manage.py load_docs

# Query
curl -X POST http://localhost:8000/api/assistant/ \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question"}'
```

## Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key
```
