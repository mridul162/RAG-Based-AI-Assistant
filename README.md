# Multilingual RAG-Based AI Assistant for E-Commerce

## Overview

This project is a production-oriented multilingual Retrieval-Augmented Generation (RAG) AI assistant designed for an organic food e-commerce business.

The system supports:

* English queries
* Bengali queries
* Banglish (Bangla written in English characters)
* Semantic product retrieval
* WhatsApp-based AI interaction
* Modular ingestion pipelines
* FAISS vector search
* PostgreSQL conversation analytics
* Cloud deployment using Render

The architecture focuses on:

* retrieval-first design
* modular engineering
* scalable ingestion
* multilingual semantic search
* lightweight deployment
* production-oriented backend APIs

---

# Features

## AI / RAG Features

* Retrieval-Augmented Generation (RAG)
* Semantic retrieval using FAISS
* OpenAI embedding integration
* OpenAI response generation
* Prompt orchestration pipeline
* Multilingual retrieval support
* Product-aware semantic search
* Retrieval source tracking

---

## Knowledge Base Features

* Markdown-based KB
* YAML product metadata
* Canonical product structure
* Retrieval-first content organization
* Incremental indexing philosophy
* Partial re-embedding strategy
* Heading-aware semantic chunking

---

## Backend Features

* FastAPI backend
* WhatsApp Cloud API integration
* PostgreSQL conversation persistence
* Dashboard analytics APIs
* Structured logging
* Dependency injection
* Environment-based configuration
* Modular service architecture

---

## Deployment Features

* Render deployment
* PostgreSQL cloud database
* Lightweight OpenAI embedding workflow
* Memory-optimized deployment
* Production-ready webhook architecture

---

# Tech Stack

## AI / RAG

* OpenAI API
* FAISS
* Semantic Retrieval
* Prompt Engineering
* Retrieval-Augmented Generation (RAG)

---

## Backend

* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL
* Requests

---

## Infrastructure

* Render
* GitHub
* Docker (optional)

---

## Data & Processing

* YAML
* Markdown
* NumPy
* Pandas

---

# Project Architecture

```text
RAG-Based-AI-Assistant/
│
├── api/
│   ├── core/
│   ├── db/
│   ├── dependencies/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── app.py
│
├── ingestion/
│   ├── chunkers/
│   ├── embedders/
│   ├── loaders/
│   ├── parsers/
│   ├── pipelines/
│   ├── utils/
│   ├── validators/
│   └── vectorstores/
│
├── retrieval/
│   └── retriever.py
│
├── knowledge_base/
│   └── catalog/
│
├── artifacts/
│   ├── chunked/
│   ├── embeddings/
│   ├── faiss/
│   ├── parsed/
│   └── pipeline_logs/
│
├── scripts/
├── requirements.txt
└── README.md
```

---

# Retrieval Workflow

```text
User Query
    ↓
OpenAI Embedding
    ↓
FAISS Semantic Search
    ↓
Relevant Chunk Retrieval
    ↓
Prompt Construction
    ↓
OpenAI Response Generation
    ↓
Final AI Response
```

---

# WhatsApp Workflow

```text
WhatsApp User
    ↓
Webhook Endpoint
    ↓
FastAPI Backend
    ↓
RAG Retrieval Pipeline
    ↓
OpenAI Generation
    ↓
WhatsApp Response
```

---

# Knowledge Base Structure

```text
data/
│
├── catalog/
│   └── products/
│       └── honey/
│           └── sundarbans_kholisha_honey/
│               ├── overview.md
│               ├── benefits.md
│               ├── nutrition.md
│               ├── sourcing.md
│               ├── usage.md
│               └── product.yaml
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/mridul162/RAG-Based-AI-Assistant.git

cd RAG-Based-AI-Assistant
```

---

## 2. Create Virtual Environment

```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key

DATABASE_URL=your_postgresql_database_url

WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token

WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id

WHATSAPP_VERIFY_TOKEN=your_verify_token
```

---

# Build Vector Database

Run:

```powershell
python -m ingestion.pipelines.build_vector_pipeline
```

This pipeline:

* validates KB
* loads markdown files
* loads YAML metadata
* parses sections
* chunks documents
* generates embeddings
* builds FAISS index
* stores retrieval metadata

---

# Run Backend Locally

```powershell
uvicorn api.app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Render Deployment

## Start Command

```text
uvicorn api.app:app --host 0.0.0.0 --port $PORT
```

---

# Dashboard APIs

## Get Conversations

```http
GET /dashboard/conversations
```

---

## Get Analytics

```http
GET /dashboard/analytics
```

---

# WhatsApp Webhook

## Verification Endpoint

```http
GET /webhooks/whatsapp
```

---

## Incoming Message Endpoint

```http
POST /webhooks/whatsapp
```

---

# Design Philosophy

This project was built around:

* modular architecture
* retrieval-first system design
* multilingual semantic retrieval
* scalable ingestion pipelines
* production-oriented engineering
* lightweight deployment constraints
* maintainable component separation

---

# Current Capabilities

* Multilingual semantic retrieval
* Bangla product search
* Banglish query handling
* WhatsApp AI assistant
* Retrieval trace persistence
* Conversation analytics
* Semantic vector indexing
* Modular ingestion pipeline
* Cloud deployment workflow

---

# Future Improvements

* Hybrid retrieval
* Reranking pipeline
* Redis caching
* Streaming responses
* Admin dashboard frontend
* Dockerized deployment
* Kubernetes deployment
* Retrieval evaluation metrics
* Multi-agent workflow support
* Image-aware retrieval

---

# Author

Asifur Rahman Mridul

* LinkedIn: [https://www.linkedin.com/in/asifmridul](https://www.linkedin.com/in/asifmridul)
* GitHub: [https://github.com/mridul162](https://github.com/mridul162)
