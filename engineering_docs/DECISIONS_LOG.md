# DECISIONS_LOG.md

# Hasanah Mart AI Assistant — Architectural & Product Decisions Log

---

# DECISION-001 — Build a Real-World AI System Instead of Tutorial-Only Learning

## Context
The project originated from the desire to move beyond tutorials, notebooks, and isolated experimentation toward building a complete real-world AI system around an actual business.

The user wanted practical exposure to:
- production-oriented AI engineering
- RAG pipelines
- deployment
- conversational systems
- backend architecture
- AI-assisted engineering workflows

---

## Options Considered

1. Continue tutorial-based learning
2. Build toy/demo chatbot projects
3. Build a real production-oriented system around an actual business

---

## Final Decision
Build a real-world multilingual AI assistant for Hasanah Mart.

---

## Reasoning
Real-world systems expose:
- deployment challenges
- architectural decisions
- debugging workflows
- operational complexity
- retrieval quality issues
- integration problems

This path provides significantly better engineering growth than isolated tutorials.

---

## Tradeoffs Accepted
- Increased complexity
- Messier learning curve
- Production debugging overhead
- Slower conceptual clarity initially

---

## Risks
- Overwhelm from system complexity
- Heavy dependence on AI-generated code
- Shallow understanding if not reverse engineered later

---

## Future Reconsideration Conditions
None currently.

This remains the foundational philosophy of the project.

---

# DECISION-002 — Use RAG Architecture Instead of Fine-Tuning

## Context
The system needed dynamic business knowledge retrieval for product-related conversational queries.

---

## Options Considered

1. Fine-tuned model
2. Prompt-only chatbot
3. Retrieval-Augmented Generation (RAG)

---

## Final Decision
Use RAG architecture.

---

## Reasoning
RAG allows:
- dynamic knowledge updates
- no model retraining
- lower operational cost
- business-specific contextual responses
- rapid experimentation

It also aligned with the learning goal of understanding modern AI application architecture.

---

## Tradeoffs Accepted
- Retrieval complexity
- Chunking challenges
- Hallucination risks
- Retrieval quality dependency

---

## Risks
- Poor retrieval leading to incorrect responses
- Weak multilingual retrieval
- Context pollution

---

## Future Reconsideration Conditions
Possible future hybrid systems:
- RAG + fine-tuning
- memory-augmented architectures

---

# DECISION-003 — Use Markdown-Based Knowledge Base

## Context
The project required a flexible, human-readable knowledge storage system suitable for chunking and semantic retrieval.

---

## Options Considered

1. JSON-first knowledge base
2. Markdown-based knowledge base
3. Database-first knowledge storage

---

## Final Decision
Use markdown-based hierarchical knowledge organization.

---

## Reasoning
Markdown:
- is human readable
- is version controllable
- supports semantic organization
- is chunk-friendly
- simplifies manual content editing

The hierarchical structure also supports semantic isolation.

---

## Tradeoffs Accepted
- No strict schema enforcement
- Potential formatting inconsistency
- Manual structure management

---

## Risks
- Content inconsistency
- Retrieval fragmentation
- Scaling challenges for large datasets

---

## Future Reconsideration Conditions
May evolve into:
- hybrid markdown + database system
- structured metadata layer
- CMS-backed knowledge system

---

# DECISION-004 — Organize Knowledge Base by Product Categories

## Context
The knowledge base required clean semantic organization for retrieval quality.

---

## Options Considered

1. One large combined document
2. Flat file structure
3. Category-based hierarchical structure

---

## Final Decision
Use category and product-based hierarchy.

---

## Reasoning
Improves:
- semantic isolation
- retrieval precision
- maintainability
- chunk clarity

---

## Tradeoffs Accepted
- More files to manage
- Higher organizational complexity

---

## Risks
- Inconsistent categorization
- Duplicate knowledge across files

---

## Future Reconsideration Conditions
Possible future:
- metadata-driven retrieval
- taxonomy-based search

---

# DECISION-005 — Use FastAPI as Backend Framework

## Context
The backend required:
- API support
- webhook support
- dependency injection
- modern architecture
- scalability potential

---

## Options Considered

1. Flask
2. Django
3. FastAPI

---

## Final Decision
Use FastAPI.

---

## Reasoning
FastAPI provides:
- async capability
- strong typing
- automatic OpenAPI docs
- clean dependency injection
- modern Python architecture

It also aligns strongly with modern AI backend engineering.

---

## Tradeoffs Accepted
- Slightly steeper learning curve
- More architectural complexity

---

## Risks
- Async misuse
- Complexity for beginners

---

## Future Reconsideration Conditions
None currently.

FastAPI remains strategically aligned.

---

# DECISION-006 — Use FAISS as Initial Vector Database

## Context
The project required semantic similarity retrieval.

---

## Options Considered

1. Pinecone
2. Weaviate
3. pgvector
4. FAISS

---

## Final Decision
Use FAISS initially.

---

## Reasoning
FAISS:
- is lightweight
- easy for experimentation
- requires minimal infrastructure
- supports rapid local prototyping

---

## Tradeoffs Accepted
- Limited scalability
- No metadata-native filtering
- No distributed architecture

---

## Risks
- Scaling limitations
- Operational complexity later

---

## Future Reconsideration Conditions
Potential migration to:
- pgvector
- Qdrant
- Weaviate
- Pinecone

---

# DECISION-007 — Use OpenAI Hosted Models Instead of Self-Hosted LLMs

## Context
The project required reliable LLM inference and embeddings.

---

## Options Considered

1. Self-hosted open-source models
2. OpenAI APIs

---

## Final Decision
Use OpenAI APIs.

---

## Reasoning
OpenAI provides:
- fast iteration
- strong multilingual support
- low infrastructure complexity
- production-grade reliability

---

## Tradeoffs Accepted
- API dependency
- token costs
- vendor lock-in

---

## Risks
- API pricing changes
- rate limits
- external dependency

---

## Future Reconsideration Conditions
Possible future:
- local inference
- open-source models
- hybrid inference architecture

---

# DECISION-008 — Use GPT-4.1-mini for Response Generation

## Context
The system required cost-effective conversational generation.

---

## Options Considered

1. Larger GPT models
2. GPT-4.1-mini

---

## Final Decision
Use GPT-4.1-mini.

---

## Reasoning
Balanced:
- speed
- cost
- response quality

Suitable for conversational commerce prototype stage.

---

## Tradeoffs Accepted
- Reduced reasoning depth
- Potentially weaker complex reasoning

---

## Risks
- Quality degradation in advanced queries

---

## Future Reconsideration Conditions
May upgrade to:
- larger GPT models
- hybrid model routing

---

# DECISION-009 — Use Streamlit for Initial Frontend

## Context
A lightweight testing interface was required quickly.

---

## Options Considered

1. React/Next.js
2. Streamlit
3. No frontend

---

## Final Decision
Use Streamlit for experimentation frontend.

---

## Reasoning
Streamlit enables:
- rapid prototyping
- fast iteration
- easy API testing
- retrieval experimentation

---

## Tradeoffs Accepted
- Limited scalability
- Less professional UI
- Minimal frontend architecture

---

## Risks
- Poor production UX
- Architectural limitations

---

## Future Reconsideration Conditions
Planned future migration toward:
- Next.js dashboard
- dedicated admin frontend

---

# DECISION-010 — Use WhatsApp as Primary User Interface

## Context
The target business audience primarily uses WhatsApp.

---

## Options Considered

1. Web-first chatbot
2. Mobile app
3. WhatsApp-first conversational interface

---

## Final Decision
Use WhatsApp Cloud API integration.

---

## Reasoning
WhatsApp:
- matches target user behavior
- enables conversational commerce
- lowers adoption friction
- supports real-world validation

---

## Tradeoffs Accepted
- API dependency
- webhook complexity
- messaging constraints

---

## Risks
- WhatsApp API policy changes
- rate limits
- webhook reliability issues

---

## Future Reconsideration Conditions
Possible future:
- multi-channel support
- website chat widget
- mobile application

---

# DECISION-011 — Keep Frontend and Backend Decoupled

## Context
The architecture needed flexibility for multiple interfaces.

---

## Options Considered

1. Monolithic frontend/backend
2. Decoupled API architecture

---

## Final Decision
Use centralized FastAPI backend with multiple client interfaces.

---

## Reasoning
Enables:
- multiple interfaces
- cleaner architecture
- independent frontend evolution
- better scalability

---

## Tradeoffs Accepted
- Additional API layer complexity

---

## Risks
- Synchronization issues
- API contract maintenance

---

## Future Reconsideration Conditions
None currently.

---

# DECISION-012 — Deploy Using Render Initially

## Context
The project required simple production deployment.

---

## Options Considered

1. AWS
2. GCP
3. Railway
4. Render

---

## Final Decision
Use Render initially.

---

## Reasoning
Render provides:
- fast deployment
- easy environment setup
- low operational overhead
- beginner-friendly deployment workflow

---

## Tradeoffs Accepted
- Less infrastructure flexibility
- Potential scaling limitations

---

## Risks
- Cold starts
- limited operational control

---

## Future Reconsideration Conditions
Potential future migration:
- AWS
- GCP
- Kubernetes

---

# DECISION-013 — Use PostgreSQL for Persistent Storage

## Context
The system required conversation persistence and analytics capability.

---

## Options Considered

1. SQLite
2. MongoDB
3. PostgreSQL

---

## Final Decision
Use PostgreSQL.

---

## Reasoning
PostgreSQL:
- production-grade
- scalable
- analytics-friendly
- supports future pgvector migration

---

## Tradeoffs Accepted
- More setup complexity
- operational overhead

---

## Risks
- schema rigidity
- scaling challenges later

---

## Future Reconsideration Conditions
Possible future:
- Redis integration
- analytics warehouse
- pgvector hybrid architecture

---

# DECISION-014 — Prioritize Backend + RAG Understanding Over Advanced Frontend Development

## Context
The user needed to decide between:
- frontend expansion
- deeper backend/RAG/system understanding

---

## Options Considered

1. Focus heavily on frontend
2. Focus deeply on backend/RAG/system architecture

---

## Final Decision
Prioritize backend + RAG + system understanding.

---

## Reasoning
AI engineering roles heavily emphasize:
- backend systems
- retrieval systems
- orchestration
- deployment
- scalability

Frontend should support the AI engineering path rather than dominate it.

---

## Tradeoffs Accepted
- Slower UI sophistication
- less polished frontend initially

---

## Risks
- weaker frontend engineering exposure

---

## Future Reconsideration Conditions
Frontend sophistication may increase after deeper system understanding.

---

# DECISION-015 — Reverse Engineer Existing System Instead of Full Immediate Rewrite

## Context
The project evolved through heavy AI-assisted coding and required deeper understanding.

---

## Options Considered

1. Rewrite entire system immediately
2. Reverse engineer and optimize existing system progressively

---

## Final Decision
Reverse engineer existing architecture first.

---

## Reasoning
The current system already contains:
- real integrations
- deployment experience
- operational exposure
- debugging history

These provide valuable learning opportunities.

---

## Tradeoffs Accepted
- Existing technical debt remains temporarily
- Architectural imperfections persist

---

## Risks
- Carrying inefficient patterns forward

---

## Future Reconsideration Conditions
Selective subsystem rewrites planned after deeper understanding.

---

# DECISION-016 — Reverse Engineer System in Original Build Sequence

## Context
Needed strategy for deeply understanding the architecture.

---

## Options Considered

1. Request-flow tracing first
2. Reverse engineering in original construction order

---

## Final Decision
Follow original construction sequence.

---

## Reasoning
Understanding system evolution layer-by-layer:
- reinforces mental models
- clarifies architectural dependencies
- improves engineering intuition

Sequence:
1. Knowledge base
2. Chunking
3. Embeddings
4. Vector DB
5. Retrieval
6. Prompting
7. Backend
8. WhatsApp
9. Persistence
10. Deployment

---

## Tradeoffs Accepted
- Less operationally-oriented initially

---

## Risks
- Slower debugging intuition initially

---

## Future Reconsideration Conditions
Later phases may focus more heavily on runtime execution tracing.

---

# DECISION-017 — Maintain Streamlit as Internal AI Testing Interface

## Context
Needed role definition for Streamlit frontend.

---

## Options Considered

1. Use Streamlit as primary production UI
2. Use Streamlit as experimentation/testing layer

---

## Final Decision
Use Streamlit primarily for testing and experimentation.

---

## Reasoning
Streamlit is highly effective for:
- prompt testing
- retrieval debugging
- multilingual testing
- rapid experimentation

---

## Tradeoffs Accepted
- Limited production UX

---

## Risks
- Misusing Streamlit beyond intended scope

---

## Future Reconsideration Conditions
Production frontend may migrate to:
- Next.js
- dedicated dashboard architecture

---

# DECISION-018 — Clean Repository for Professional Portfolio Presentation

## Context
Repository contained noisy development artifacts.

---

## Options Considered

1. Keep raw repository
2. Clean and architecture-orient repository

---

## Final Decision
Refactor repository structure for professional presentation.

---

## Reasoning
Professional repositories signal:
- engineering maturity
- architectural thinking
- maintainability

---

## Tradeoffs Accepted
- Additional maintenance effort

---

## Risks
- Over-cleaning useful artifacts

---

## Future Reconsideration Conditions
Repository structure may evolve as system scales.

---

# DECISION-019 — Use WhatsApp Internal Production Validation Before Full Production Hardening

## Context
Needed practical validation before deep optimization.

---

## Options Considered

1. Complete production hardening first
2. Validate real-world usage early

---

## Final Decision
Start real user testing early through WhatsApp.

---

## Reasoning
Real-world interaction exposes:
- retrieval weaknesses
- UX problems
- conversational issues
- operational bottlenecks

Much faster than isolated engineering refinement.

---

## Tradeoffs Accepted
- Prototype instability
- architectural imperfections visible early

---

## Risks
- poor user experience
- operational inconsistencies

---

## Future Reconsideration Conditions
Production hardening becomes priority after validation insights accumulate.

---

# DECISION-020 — Treat the Project as an AI Engineering Sandbox Rather Than Only a Business Tool

## Context
The project evolved beyond simple chatbot implementation.

---

## Options Considered

1. Optimize only for business utility
2. Use project as AI engineering learning platform

---

## Final Decision
Treat project as both:
- business assistant
- AI engineering sandbox

---

## Reasoning
The project provides valuable exposure to:
- backend engineering
- AI orchestration
- retrieval systems
- deployment
- production workflows

---

## Tradeoffs Accepted
- slower direct business optimization
- more experimentation

---

## Risks
- overengineering
- shifting focus away from business outcomes

---

## Future Reconsideration Conditions
Business optimization may become stronger focus once engineering foundations mature.

---