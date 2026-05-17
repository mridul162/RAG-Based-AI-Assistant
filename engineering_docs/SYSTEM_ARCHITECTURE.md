````markdown id="3h4wqp"
# SYSTEM_ARCHITECTURE.md

# Hasanah Mart AI Assistant — System Architecture Documentation

---

# 1. System Overview

## 1.1 Purpose of the System

The Hasanah Mart AI Assistant is a production-oriented multilingual Retrieval-Augmented Generation (RAG) conversational commerce system designed for an organic food business operating in Bangladesh.

The system aims to:
- Automate customer interaction
- Provide AI-powered product consultation
- Enable multilingual conversational commerce
- Support WhatsApp-based customer communication
- Build operational understanding of production-grade AI systems
- Serve as a real-world experimentation platform for AI engineering

The architecture was intentionally designed to expose the complete lifecycle of modern AI system engineering:
- Knowledge base design
- Embedding generation
- Semantic retrieval
- Prompt orchestration
- LLM integration
- Real-time messaging
- Persistence
- Analytics
- Deployment

---

# 1.2 High-Level Architecture

```text
                        ┌──────────────────────┐
                        │   Knowledge Base     │
                        │  Markdown Documents  │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ Embedding Pipeline   │
                        │ OpenAI Embeddings    │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │   FAISS Vector DB    │
                        │ Semantic Index Store │
                        └──────────┬───────────┘
                                   │
                                   ▼
┌───────────────┐       ┌──────────────────────┐
│ WhatsApp API  │──────▶│   FastAPI Backend    │
└───────────────┘       │                      │
                        │  - Webhook Handler   │
┌───────────────┐       │  - RAG Service       │
│  Streamlit UI │──────▶│  - Dashboard APIs    │
└───────────────┘       │  - Persistence Layer │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │     OpenAI API       │
                        │ GPT-4.1-mini         │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │   PostgreSQL DB      │
                        │ Conversations Store  │
                        └──────────────────────┘
````

---

# 1.3 Core Workflows

## Primary Workflows

1. WhatsApp conversational flow
2. Streamlit conversational testing flow
3. RAG retrieval pipeline
4. Embedding generation pipeline
5. Conversation persistence pipeline
6. Analytics API flow
7. Deployment lifecycle

---

# 2. Architecture Components

---

# 2.1 Frontend Layer

## Current Frontend

### Streamlit Frontend

Purpose:

* Rapid experimentation
* Internal testing
* Prompt testing
* Retrieval debugging
* Public prototype demo

Responsibilities:

* Query submission
* Display AI responses
* Manual multilingual testing

Communication:

* Calls FastAPI `/chat/ask`

Deployment:

* Separate Render service

Limitations:

* Not production-grade UI
* Limited scalability
* Minimal state management

---

# 2.2 Backend Layer

## Backend Framework

### FastAPI

Responsibilities:

* API orchestration
* Request validation
* Service lifecycle management
* Webhook handling
* RAG orchestration
* Analytics APIs

Key Characteristics:

* Modular architecture
* Dependency injection
* Lifecycle-managed services
* Pydantic validation
* Swagger/OpenAPI docs

Main Components:

* Routes
* Services
* Schemas
* Core config
* DB layer

---

# 2.3 Database Layer

## Primary Database

### PostgreSQL

Purpose:

* Persistent conversation storage
* Analytics
* Operational monitoring

Current Stored Data:

* User phone number
* User query
* AI response
* Timestamp

ORM:

* SQLAlchemy

Current Limitations:

* Basic schema
* No advanced indexing
* No partitioning
* No analytics optimization

Future Possibilities:

* User memory
* Session management
* Conversation analytics
* Order tracking

---

# 2.4 Vector Database Layer

## Current Vector Store

### FAISS

Purpose:

* Semantic similarity search
* Retrieval of relevant knowledge chunks

Stored Artifacts:

* Vector embeddings
* Metadata mappings

Files:

* `faiss_index.index`
* `chunks_metadata.pkl`

Current Retrieval Strategy:

* Top-k semantic retrieval

Limitations:

* No metadata filtering
* No hybrid search
* No reranking
* In-memory/local architecture

Future Possibilities:

* pgvector
* Weaviate
* Pinecone
* Hybrid retrieval

---

# 2.5 RAG Pipeline

## Pipeline Stages

### Stage 1 — Query Reception

Input:

* User query from WhatsApp or Streamlit

### Stage 2 — Query Embedding

Model:

* `text-embedding-3-small`

### Stage 3 — Semantic Retrieval

Engine:

* FAISS

Operation:

* Similarity search against indexed knowledge chunks

### Stage 4 — Context Selection

Operation:

* Select top-k chunks

### Stage 5 — Prompt Construction

Operation:

* Inject retrieved context into prompt template

### Stage 6 — Response Generation

Model:

* GPT-4.1-mini

### Stage 7 — Response Delivery

Targets:

* WhatsApp
* Streamlit
* API response

---

# 2.6 APIs

## Chat API

### Endpoint

```text
POST /chat/ask
```

Purpose:

* General conversational interaction
* Streamlit frontend integration

Flow:

1. Validate request
2. Call RAG service
3. Return structured response

---

## WhatsApp Webhook

### Endpoints

```text
GET /webhooks/whatsapp
POST /webhooks/whatsapp
```

Responsibilities:

* Meta webhook verification
* Incoming message handling
* Reply orchestration

---

## Dashboard APIs

### Endpoints

```text
GET /dashboard/conversations
GET /dashboard/conversations/{id}
GET /dashboard/analytics
```

Purpose:

* Monitoring
* Analytics
* Internal operations

---

# 2.7 Authentication & Security

## Current State

Minimal authentication.

Current Security:

* Environment variable secrets
* `.env` exclusion
* Token-based API integrations

Missing Components:

* User authentication
* Admin authentication
* RBAC
* Rate limiting
* Request verification hardening

Security Risks:

* Webhook abuse
* Token exposure
* Public endpoint misuse

---

# 2.8 WhatsApp Integration

## Platform

WhatsApp Cloud API

## Components

* Meta Developer App
* Webhooks
* Message send API

## Flow

```text
User Message
    ↓
WhatsApp Cloud API
    ↓
Webhook POST
    ↓
FastAPI Webhook Handler
    ↓
RAG Pipeline
    ↓
AI Response
    ↓
WhatsApp Send API
    ↓
User Receives Reply
```

Current State:

* Functional
* Real-time responses
* Production prototype

Limitations:

* Synchronous processing
* No retry queues
* No idempotency layer

---

# 2.9 AI Components

## Embedding Model

### OpenAI `text-embedding-3-small`

Purpose:

* Semantic representation
* Similarity search

Reasons Chosen:

* Affordable
* Lightweight
* Good multilingual support

Tradeoffs:

* Smaller embedding quality vs larger models

---

## LLM Model

### OpenAI `gpt-4.1-mini`

Purpose:

* Final response generation

Reasons Chosen:

* Cost efficiency
* Faster inference
* Sufficient for conversational commerce prototype

Tradeoffs:

* Less reasoning depth vs larger GPT models

---

# 2.10 Storage Systems

## Knowledge Storage

Markdown document hierarchy.

## Vector Storage

FAISS local index.

## Persistent Storage

PostgreSQL.

## Log Storage

Text log files.

---

# 2.11 File Structures

## Current Backend Structure

```text
api/
├── core/
│   ├── config.py
│   └── logging.py
│
├── routes/
│   ├── chat.py
│   └── whatsapp.py
│
├── services/
│   ├── rag_service.py
│   └── whatsapp_service.py
│
├── schemas/
│
├── db/
│   ├── database.py
│   ├── models.py
│   └── crud.py
│
└── dependencies/
```

---

## Knowledge Base Structure

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

---

# 3. Data Flow

---

# 3.1 User Query Flow

```text
User
    ↓
WhatsApp / Streamlit
    ↓
FastAPI Route
    ↓
Request Validation
    ↓
RAG Service
    ↓
Retrieval Pipeline
    ↓
OpenAI Response
    ↓
Persistence
    ↓
User Reply
```

---

# 3.2 Retrieval Flow

```text
User Query
    ↓
Query Embedding
    ↓
FAISS Similarity Search
    ↓
Top-k Chunk Retrieval
    ↓
Context Aggregation
```

---

# 3.3 Embedding Flow

```text
Markdown Documents
    ↓
Chunking Pipeline
    ↓
Embedding Generation
    ↓
Vector Serialization
    ↓
FAISS Index Storage
```

---

# 3.4 Response Generation Flow

```text
Retrieved Context
    +
User Query
    ↓
Prompt Builder
    ↓
GPT-4.1-mini
    ↓
Generated Response
```

---

# 3.5 Knowledge Base Update Flow

```text
New Product Content
    ↓
Markdown Update
    ↓
Chunk Regeneration
    ↓
Embedding Regeneration
    ↓
FAISS Reindexing
```

---

# 4. Technical Decisions

---

# 4.1 Why FastAPI

Reasons:

* Async capability
* Modern architecture
* Dependency injection
* Automatic docs
* Strong typing support

Alternative Considered:

* Flask

Tradeoff:

* Slightly steeper learning curve

---

# 4.2 Why Markdown Knowledge Base

Reasons:

* Human readable
* Easy organization
* Chunk-friendly
* Version controllable

Tradeoffs:

* No schema enforcement
* Potential inconsistency

---

# 4.3 Why FAISS

Reasons:

* Lightweight
* Fast experimentation
* Local simplicity

Tradeoffs:

* Limited operational scalability
* No metadata-native filtering

---

# 4.4 Why WhatsApp

Reasons:

* Real business use case
* User accessibility
* Conversational commerce focus

---

# 4.5 Why Streamlit

Reasons:

* Rapid prototyping
* Fast testing
* Low frontend overhead

Tradeoffs:

* Not ideal for large-scale production UI

---

# 5. Infrastructure

---

# 5.1 Hosting

## Current

Render.

## Services

* FastAPI backend service
* Streamlit frontend service
* PostgreSQL managed database

---

# 5.2 Deployment

## Current Deployment Style

Dockerized deployment.

## Components

* Dockerfile
* Environment variables
* Render deployment

---

# 5.3 Environment Setup

## Important Variables

```env
OPENAI_API_KEY=
WHATSAPP_VERIFY_TOKEN=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
DATABASE_URL=
```

---

# 5.4 Local Development

## Backend

```bash
uvicorn api.app:app --reload
```

## Streamlit

```bash
streamlit run frontend/app.py
```

---

# 5.5 CI/CD

## Current State

No formal CI/CD pipeline.

## Possible Future Additions

* GitHub Actions
* Automated testing
* Automated deployment
* Linting
* Security scanning

---

# 6. Scalability Considerations

## Current Bottlenecks

### Synchronous Request Handling

Problem:

* OpenAI calls block request lifecycle

### No Queue System

Problem:

* WhatsApp spikes may overload backend

### Local FAISS

Problem:

* Single-instance architecture

### No Caching

Problem:

* Repeated embedding/retrieval costs

---

# 7. Cost Considerations

## Current Cost Drivers

* OpenAI API calls
* Embeddings
* Chat completions
* Render hosting
* PostgreSQL hosting

## Current Optimization Strategy

* Use `gpt-4.1-mini`
* Use smaller embedding model
* Lightweight infrastructure

---

# 8. Known Technical Challenges

---

# 8.1 Current Bottlenecks

* Retrieval quality
* Multilingual retrieval consistency
* No observability layer
* No async orchestration
* No reranking
* No hybrid retrieval

---

# 8.2 Technical Debt

* AI-generated architecture without full internalization
* Minimal testing infrastructure
* Limited auth/security
* Prototype-grade deployment patterns

---

# 8.3 Risks

* Hallucinations
* Token leakage
* Scaling limitations
* Operational instability under load

---

# 8.4 Unresolved Issues

* Conversation memory
* Session continuity
* Human escalation
* Evaluation framework
* Production-grade monitoring

---

# 9. Future Architecture Evolution

---

# 9.1 Backend Evolution

Possible:

* Async workers
* Queue architecture
* Microservice separation

Technologies:

* Celery
* Redis
* RabbitMQ

---

# 9.2 Retrieval Evolution

Possible:

* Hybrid retrieval
* Metadata filtering
* Reranking
* pgvector migration

---

# 9.3 Frontend Evolution

Possible:

* Next.js dashboard
* Admin operations UI
* Analytics visualization

---

# 9.4 AI Evolution

Possible:

* Tool calling
* Memory systems
* Structured outputs
* Agent workflows

---

# 9.5 Observability Evolution

Possible:

* OpenTelemetry
* Latency dashboards
* Retrieval inspection
* Token monitoring

---

# 9.6 Infrastructure Evolution

Possible:

* Kubernetes
* Managed vector DB
* CDN
* Multi-region deployment

---

# 10. Architectural Philosophy

The system intentionally prioritizes:

* real-world experimentation
* modular architecture
* production-oriented exposure
* practical AI engineering learning

The project serves both as:

1. A functional conversational commerce system
2. A sandbox for reverse engineering production-grade AI systems

The long-term objective is to transition from:

* AI-assisted feature building

toward:

* deep architectural understanding
* scalable AI engineering
* production-grade system design

---

```
```
