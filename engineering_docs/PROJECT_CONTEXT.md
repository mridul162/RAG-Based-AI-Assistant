````markdown
# PROJECT_CONTEXT.md

# Hasanah Mart AI Assistant — Master Project Context

## 1. Overview

### Project Name
Hasanah Mart AI Assistant

### Project Type
Production-oriented multilingual RAG-powered conversational commerce assistant.

### Core Purpose
Build a real-world AI assistant around an actual organic food business (Hasanah Mart) to:

- Learn applied AI engineering
- Understand production-oriented RAG systems
- Gain backend/system engineering experience
- Experiment with AI-assisted software development
- Build multilingual conversational commerce capability
- Explore production deployment workflows

---

# 2. Business Context

## Business Name
Hasanah Mart

## Business Domain
Organic / safe food e-commerce business in Bangladesh.

## Product Categories
- Honey
- Ghee
- Dates
- Mixed nuts
- Fruits
- Coconut oil
- Seeds
- Other organic foods

## Business Goals
- Automate customer interaction
- Provide product consultation
- Enable multilingual conversational commerce
- Support AI-based customer engagement
- Build future AI sales assistant capability
- Build future AI order assistant capability
- Improve customer support scalability

---

# 3. Project Objective

## Technical Objective
Build a modular end-to-end RAG system integrating:

- Knowledge base
- Embedding pipeline
- Semantic retrieval
- LLM orchestration
- API backend
- WhatsApp integration
- Persistent storage
- Analytics layer
- Dashboard APIs
- Frontend experimentation interface

---

# 4. Target Users

## Current Internal Users
- Project owner
- Partners
- Family members
- Internal testers

## Future External Users
- Hasanah Mart customers
- WhatsApp users
- Organic food buyers
- Bengali-speaking customers

---

# 5. Current State

## Overall Status
Prototype / internal production validation phase.

## Working Components
- FastAPI backend
- RAG pipeline
- OpenAI integration
- FAISS vector search
- WhatsApp Cloud API integration
- Streamlit frontend
- PostgreSQL persistence
- Dashboard APIs
- Docker deployment
- Render deployment

## Current Focus
Reverse engineering and deeply understanding the existing system architecture.

---

# 6. System Architecture

## High-Level Flow

```text
User Query (WhatsApp / Streamlit)
    ↓
FastAPI Endpoint (/chat/ask or Webhook)
    ↓
Pydantic Request Validation
    ↓
Dependency Injection
    ↓
RAG Service Layer
    ↓
Query Embedding Generation
    ↓
FAISS Semantic Retrieval
    ↓
Relevant Chunk Selection
    ↓
Prompt Construction
    ↓
OpenAI Response Generation
    ↓
Structured API Response
    ↓
WhatsApp / Streamlit Response Delivery
    ↓
Conversation Persistence (PostgreSQL)
    ↓
Dashboard Analytics APIs
    ↓
Logging + Latency Tracking
    ↓
Dockerized Cloud Deployment
````

---

# 7. Technologies Used

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy

## AI / LLM

* OpenAI API
* GPT-4.1-mini
* text-embedding-3-small

## Retrieval

* FAISS
* Semantic search

## Database

* PostgreSQL

## Frontend

* Streamlit

## Messaging

* WhatsApp Cloud API
* Meta Developer Platform
* Webhooks

## Deployment

* Docker
* Render

## Utilities

* dotenv
* httpx
* requests

---

# 8. Current Folder Structure

```text
RAG-System-for-Hasanah-Mart/
│
├── api/
│   ├── core/                 # Config, logging, settings
│   ├── routes/               # API routes & webhook handlers
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # RAG & WhatsApp services
│   ├── db/                   # Database models & CRUD
│   └── dependencies/         # Dependency injection
│
├── data/                     # Knowledge base
│
├── frontend/                 # Streamlit frontend
│
├── notebooks/                # Experimentation
│
├── vector_db/                # FAISS index & metadata
│
├── logs/                     # Application logs
│
├── Dockerfile
├── render.yaml
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── .dockerignore
```

---

# 9. Naming Conventions

## API Layer

* `routes/`
* `services/`
* `schemas/`
* `db/`
* `core/`

## Services

Examples:

* `rag_service.py`
* `whatsapp_service.py`

## Routes

Examples:

* `chat.py`
* `whatsapp.py`

## Database

Examples:

* `database.py`
* `crud.py`

---

# 10. Knowledge Base Structure

## Current Approach

Markdown-based hierarchical product knowledge base.

## Example Structure

```text
data/
├── catalog/
│   ├── products/
│   │   ├── honey/
│   │   │   ├── sundarbans_kholisha/
│   │   │   │   ├── overview.md
│   │   │   │   ├── nutrition.md
│   │   │   │   ├── benefits.md
│   │   │   │   ├── sourcing.md
```

## Design Intent

* Semantic isolation
* Better chunking
* Cleaner retrieval
* Product-specific context

---

# 11. Data Formats

## Knowledge Base

* Markdown (`.md`)

## Vector Metadata

* Pickle (`.pkl`)

## Vector Index

* FAISS index file (`.index`)

## API Communication

* JSON

## Logging

* Structured text logs

---

# 12. Core Features

## Current Features

* RAG-based semantic retrieval
* Multilingual support
* WhatsApp conversational interface
* Streamlit testing frontend
* Persistent conversation storage
* Dashboard APIs
* Structured logging
* Deployment pipeline

## Planned Features

* AI sales assistant
* AI customer support
* AI order assistant
* Product consultant
* Analytics dashboard
* Human escalation
* Conversation memory
* Retrieval observability
* Queue-based processing

---

# 13. APIs & Endpoints

## Chat Endpoint

```text
POST /chat/ask
```

Purpose:

* Streamlit frontend
* Manual testing
* API access

---

## WhatsApp Webhook

```text
GET /webhooks/whatsapp
POST /webhooks/whatsapp
```

Purpose:

* Webhook verification
* Incoming message handling

---

## Dashboard APIs

```text
GET /dashboard/conversations
GET /dashboard/conversations/{id}
GET /dashboard/analytics
```

Purpose:

* Monitoring
* Analytics
* Conversation inspection

---

# 14. Prompt Engineering Strategy

## Current Strategy

Basic RAG context injection.

## Workflow

1. Retrieve top-k chunks
2. Build prompt with retrieved context
3. Inject user query
4. Generate final response

## Current Limitations

* No reranking
* No hybrid retrieval
* No advanced context compression
* No hallucination evaluation pipeline

## Planned Improvements

* Better prompt templates
* Structured prompting
* Retrieval-aware prompting
* Context filtering
* Hallucination reduction

---

# 15. Multilingual Considerations

## Supported Languages

* Bengali
* English
* Banglish

## Important Challenge

Cross-language semantic retrieval quality.

## Open Questions

* Should Bengali aliases exist?
* Should transliterated keywords be added?
* How well do embeddings generalize across languages?

---

# 16. Deployment Architecture

## Backend

Render deployment.

## Frontend

Separate Streamlit deployment.

## Current Architecture

```text
                FastAPI Backend
              (RAG + OpenAI + DB)
                     |
     -----------------------------------
     |                |                |
 WhatsApp        Streamlit        Dashboard
 Interface        Testing UI       Admin UI
```

---

# 17. Security Considerations

## Important Secrets

* OPENAI_API_KEY
* WHATSAPP_ACCESS_TOKEN
* DATABASE_URL

## Security Practices

* `.env` excluded from GitHub
* `.gitignore` configured
* Tokens rotated if exposed

## Risks

* Public exposure of access tokens
* Webhook abuse
* Lack of authentication layer
* No rate limiting yet

---

# 18. Performance Considerations

## Current Bottlenecks

* Synchronous request handling
* No caching
* No queue system
* Retrieval latency
* OpenAI response latency

## Future Optimizations

* Async processing
* Redis caching
* Background workers
* Hybrid retrieval
* Better chunking
* Retrieval reranking

---

# 19. UX Considerations

## Current UX

* WhatsApp-first interaction
* Streamlit experimentation UI

## Important UX Goals

* Natural conversational flow
* Multilingual usability
* Fast response time
* Product-specific accuracy

## Future UX Plans

* Admin dashboard
* Better frontend
* Next.js dashboard
* Conversation monitoring

---

# 20. Logging & Observability

## Current Logging

Structured logging using Python logging.

## Current Metrics

* Request lifecycle
* Retrieval timing
* OpenAI timing

## Planned Observability

* Token tracking
* Latency dashboards
* Retrieval inspection
* Failure monitoring

---

# 21. Completed Tasks

## Backend

* FastAPI backend
* Dependency injection
* Lifecycle management

## RAG

* Embedding pipeline
* FAISS retrieval
* Prompt construction

## WhatsApp

* Webhook verification
* Incoming message handling
* Outgoing replies

## Database

* PostgreSQL integration
* CRUD operations
* Conversation persistence

## Frontend

* Streamlit frontend

## Deployment

* Dockerization
* Render deployment

---

# 22. Pending Tasks

## Short-Term

* Reverse engineer existing architecture
* Deeply understand each layer
* Improve retrieval quality
* Add observability

## Mid-Term

* Dashboard frontend
* Better analytics
* Improved multilingual retrieval

## Long-Term

* Production scaling
* Async orchestration
* Queue systems
* AI sales automation

---

# 23. Reverse Engineering Roadmap

## Current Phase

Phase RE-1 — Knowledge Base Layer

## Planned Reverse Engineering Sequence

### RE-1 — Knowledge Base Layer

Focus:

* Semantic organization
* Chunkability
* Information architecture

### RE-2 — Chunking Pipeline

Focus:

* Chunk size
* Overlap
* Semantic boundaries

### RE-3 — Embeddings Layer

Focus:

* Embedding behavior
* Similarity representation

### RE-4 — Vector Database

Focus:

* FAISS internals
* Similarity search

### RE-5 — Retrieval Pipeline

Focus:

* Retrieval quality
* Ranking behavior

### RE-6 — Prompt Layer

Focus:

* Context injection
* Prompt optimization

### RE-7 — Backend Architecture

Focus:

* FastAPI
* Dependency injection
* Lifecycle management

### RE-8 — WhatsApp Integration

Focus:

* Webhooks
* Orchestration

### RE-9 — Persistence & Analytics

Focus:

* Database architecture
* Observability

### RE-10 — Deployment & Scaling

Focus:

* Docker
* Production architecture
* Scalability

---

# 24. Important Decisions

## Decision

Use FastAPI instead of Flask.

Reason:

* Better async support
* Cleaner architecture
* Automatic docs
* Better production ergonomics

---

## Decision

Use markdown knowledge base.

Reason:

* Human readable
* Chunk-friendly
* Easy organization

---

## Decision

Use FAISS initially instead of pgvector.

Reason:

* Simpler experimentation
* Lightweight setup

---

## Decision

Use WhatsApp as primary interface.

Reason:

* Real-world conversational commerce
* Target customer accessibility

---

# 25. Risks & Bottlenecks

## Technical Risks

* Poor retrieval quality
* Hallucinations
* Scaling bottlenecks
* Token costs
* Weak multilingual retrieval

## Operational Risks

* Lack of authentication
* No rate limiting
* No queue architecture
* Synchronous request flow

## Learning Risks

* Overreliance on AI-generated code
* Shallow understanding

---

# 26. Important Constraints

## Current Constraints

* Prototype-stage architecture
* Limited observability
* No production queue system
* No advanced evaluation framework

## Personal Constraint

The project was initially built heavily with ChatGPT assistance and now requires deep reverse engineering and understanding.

---

# 27. Long-Term Vision

Transition from:

* AI-assisted prototype building

To:

* deeply understanding and engineering scalable production-grade AI systems.

Ultimate Goal:
Become highly skilled in:

* RAG engineering
* Backend architecture
* Applied AI systems
* Production AI engineering

---

# 28. Recommended Immediate Next Step

Current recommended focus:

## Phase RE-1 — Knowledge Base Analysis

Tasks:

* Analyze product knowledge structure
* Study chunkability
* Analyze semantic isolation
* Study multilingual retrieval implications
* Identify retrieval weaknesses
* Identify missing business knowledge

Do NOT optimize yet.

First:

* deeply understand
* document
* question design decisions

---

# 29. References

## Repository

[https://github.com/mridul162/RAG-System-for-Hasanah-Mart](https://github.com/mridul162/RAG-System-for-Hasanah-Mart)

## Frontend Demo

[https://hasanah-mart-streamlit.onrender.com](https://hasanah-mart-streamlit.onrender.com)

## Key External Services

* OpenAI API
* WhatsApp Cloud API
* Meta Developer Platform
* Render
* PostgreSQL

---

```
```
