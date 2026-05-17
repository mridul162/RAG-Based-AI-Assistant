# KB_DESIGN.md

# Hasanah Mart AI Assistant — Knowledge Base Design Specification

---

# 1. Purpose

This document defines the architectural philosophy, standards, conventions, and operational rules for the Hasanah Mart AI Assistant knowledge base.

The knowledge base (KB) is the foundational layer of the RAG system.

Its design directly affects:

* retrieval quality
* hallucination rate
* multilingual robustness
* chunk coherence
* prompt grounding
* scalability
* maintainability

This document establishes:

* knowledge organization standards
* retrievable knowledge boundaries
* metadata philosophy
* multilingual handling rules
* ingestion constraints
* chunking assumptions
* retrieval-oriented content design

---

# 2. Core Philosophy

The Hasanah Mart KB is designed as:

```text
Retrieval-first knowledge architecture
```

NOT:

* traditional documentation
* blog-style writing
* CMS-style article storage

The KB exists primarily to:

* maximize retrieval precision
* improve grounding fidelity
* reduce hallucinations
* support multilingual semantic retrieval

---

# 3. Fundamental Design Principles

---

# 3.1 Retrieval-Oriented Design

All knowledge must be structured for:

* semantic retrieval
* contextual isolation
* chunk coherence
* embedding quality

Content should not be optimized solely for:

* human reading flow
* long-form narrative structure

Instead optimize for:

* retrievability
* semantic clarity
* contextual independence

---

# 3.2 Semantic Isolation

Different knowledge domains should remain isolated whenever possible.

Example:

```text
benefits.md
nutrition.md
usage.md
warnings.md
```

instead of:

```text
everything_about_honey.md
```

Reason:
semantic isolation improves:

* retrieval precision
* reranking quality
* chunk coherence
* hallucination reduction

---

# 3.3 Product-Centric Architecture

The primary retrieval unit is:

```text
product
```

Knowledge should be organized around:

* categories
* products
* knowledge types

---

# 3.4 Modular Knowledge Organization

The KB should evolve incrementally.

Adding:

* products
* categories
* new knowledge types
* multilingual variants

must not require major restructuring.

---

# 3.5 Metadata-Driven Retrieval

The system should progressively evolve from:

* file-based retrieval

toward:

* metadata-aware retrieval

Metadata is considered a first-class architectural component.

---

# 4. Knowledge Base Scope

---

# 4.1 Public Retrieval Knowledge

The following content is considered safe for customer-facing retrieval:

* product information
* FAQs
* sourcing details
* authenticity information
* usage instructions
* storage instructions
* pricing explanations
* delivery information
* customer support information
* certifications
* category guides

This content may be:

* chunked
* embedded
* indexed
* retrieved

---

# 4.2 Restricted/Internal Knowledge

The following content must NEVER enter customer retrieval pipelines:

* engineering documentation
* prompts
* API secrets
* deployment configs
* internal operational notes
* architecture docs
* admin-only instructions
* debugging logs
* evaluation notes
* raw analytics

These must remain outside:

* embedding pipelines
* vector stores
* customer retrieval

---

# 5. Directory Structure

---

# 5.1 Canonical Knowledge Base Structure

```text
knowledge_base/
│
├── catalog/
│   ├── products/
│   ├── categories/
│   ├── bundles/
│   └── comparisons/
│
├── global/
│   ├── company/
│   ├── customer_support/
│   ├── conversational/
│   ├── health/
│   └── multilingual/
│
├── taxonomy/
│
└── schemas/
```

---

# 5.2 Product Structure

Each product should have its own isolated directory.

Example:

```text
products/honey/sundarbans_kholisha/
```

---

# 5.3 Canonical Product Structure

```text
sundarbans_kholisha/
│
├── product.yaml
├── overview.md
├── benefits.md
├── nutrition.md
├── sourcing.md
├── authenticity.md
├── usage.md
├── storage.md
├── faq.md
├── comparisons.md
├── warnings.md
├── certifications.md
├── pricing.md
├── shipping.md
├── aliases.md
└── testimonials.md
```

---

# 6. Knowledge Types

---

# 6.1 Standard Knowledge Types

Every product may contain the following retrieval domains:

| Knowledge Type | Purpose                      |
| -------------- | ---------------------------- |
| overview       | General introduction         |
| benefits       | Health/use benefits          |
| nutrition      | Nutritional information      |
| sourcing       | Product origin               |
| authenticity   | Purity/trust information     |
| usage          | Consumption guidance         |
| storage        | Preservation guidance        |
| faq            | Common customer questions    |
| warnings       | Safety/limitations           |
| comparisons    | Product comparisons          |
| pricing        | Pricing explanation          |
| shipping       | Delivery/shipping details    |
| certifications | Trust/compliance info        |
| testimonials   | Customer experiences         |
| aliases        | Multilingual name variations |

---

# 6.2 Knowledge Type Design Rule

Each knowledge file should ideally answer:

* one semantic intent cluster
* one retrieval category

Avoid mixing unrelated semantic domains.

---

# 7. Metadata Philosophy

---

# 7.1 Metadata Importance

Metadata is a critical retrieval architecture component.

The system should progressively evolve toward:

* metadata filtering
* retrieval reranking
* retrieval analytics
* retrieval observability

---

# 7.2 Minimum Metadata Requirements

Each chunk should eventually include:

```json
{
  "product": "",
  "category": "",
  "knowledge_type": "",
  "language": "",
  "visibility": "public",
  "retrieval_priority": 0.0,
  "source_file": "",
  "chunk_id": ""
}
```

---

# 7.3 Visibility Levels

Allowed values:

```text
public
private
internal
admin_only
```

Customer-facing retrieval systems must only retrieve:

```text
visibility=public
```

---

# 7.4 Retrieval Priority

Some knowledge may deserve higher retrieval importance.

Example:

* authenticity
* safety
* sourcing

may receive higher priority weighting later.

---

# 8. Multilingual Design

---

# 8.1 Supported Languages

The system is designed to support:

* Bengali
* English
* Banglish
* Mixed-language queries

---

# 8.2 Multilingual Challenge

Users may ask equivalent questions using:

* Bengali script
* English
* phonetic Banglish
* mixed queries

Example:

```text
খাঁটি মধু?
khati modhu?
pure honey?
ei honey original?
```

All should retrieve semantically relevant chunks.

---

# 8.3 Alias Strategy

Each product should contain:

```text
aliases.md
```

Example:

```markdown
# Bengali
- খলিশা মধু

# English
- Sundarbans Kholisha Honey

# Banglish
- kholisha modhu
- khati modhu
```

---

# 8.4 Synonym Normalization

Future multilingual normalization may include:

* transliteration maps
* typo normalization
* regional terms
* synonym dictionaries

---

# 9. Chunking Assumptions

---

# 9.1 Semantic Chunking Philosophy

Chunk boundaries should align with:

* semantic meaning
* heading structure
* intent clusters

NOT merely:

* fixed token counts

---

# 9.2 Preferred Chunk Characteristics

Good chunks should:

* contain one semantic topic
* be contextually understandable
* minimize unrelated information
* preserve grounding fidelity

---

# 9.3 Anti-Patterns

Avoid:

* giant documents
* mixed semantic topics
* duplicated information
* excessive cross-topic paragraphs

---

# 10. Retrieval Design Assumptions

---

# 10.1 Retrieval Flow

Planned retrieval pipeline:

```text
User Query
    ↓
Normalization
    ↓
Embedding
    ↓
Vector Retrieval
    ↓
Metadata Filtering
    ↓
Reranking
    ↓
Context Selection
```

---

# 10.2 Retrieval Unit

Current retrieval unit:

```text
chunk
```

Future possible retrieval units:

* semantic object
* structured retrieval document
* hybrid chunk + metadata object

---

# 10.3 Retrieval Goals

The KB should optimize for:

* high semantic recall
* high retrieval precision
* multilingual robustness
* minimal hallucination
* context relevance

---

# 11. Ingestion Rules

---

# 11.1 Allowed Ingestion Paths

Only explicitly approved KB directories should enter embedding pipelines.

Example:

```python
ALLOWED_PATHS = [
    "knowledge_base/catalog",
    "knowledge_base/global/customer_support"
]
```

---

# 11.2 Forbidden Ingestion Paths

Never embed:

```text
engineering_docs/
logs/
prompts/
evaluation/
vector_db/
```

---

# 11.3 Ingestion Validation

Future ingestion pipelines should validate:

* metadata completeness
* schema consistency
* visibility rules
* duplicate chunks
* malformed markdown

---

# 12. Content Writing Standards

---

# 12.1 Retrieval-Friendly Writing

Content should:

* use concise paragraphs
* preserve semantic clarity
* avoid excessive storytelling
* reduce ambiguity

---

# 12.2 Fact Grounding

Avoid:

* unsupported health claims
* unverifiable statements
* exaggerated marketing language

The KB should prioritize:

* factual grounding
* retrieval clarity
* customer trust

---

# 12.3 Semantic Explicitness

Important concepts should be stated explicitly.

Avoid assuming:

* implicit context
* conversational memory
* prior knowledge

---

# 13. Evaluation Considerations

---

# 13.1 Retrieval Testing

The KB must eventually support:

* retrieval benchmarks
* multilingual query tests
* hallucination analysis
* grounding evaluation

---

# 13.2 Retrieval Failure Tracking

Future evaluation should identify:

* missed retrievals
* wrong retrievals
* context pollution
* multilingual failures

---

# 14. Scalability Philosophy

The KB design should support future evolution toward:

* metadata-aware retrieval
* hybrid retrieval
* reranking
* structured retrieval objects
* analytics-driven retrieval optimization
* distributed vector infrastructure

without requiring:

* complete KB redesign
* major content migration

---

# 15. Long-Term Evolution

The current markdown-based KB is intentionally:

* simple
* inspectable
* human-editable

Future evolution may include:

* structured retrieval schemas
* CMS-backed management
* automated ingestion pipelines
* retrieval analytics systems
* knowledge governance tooling

The current design should not block these future transitions.

---

# 16. Architectural Philosophy Summary

The Hasanah Mart KB is designed as:

```text
A modular, multilingual, retrieval-first semantic knowledge system
```

NOT merely:

* a document repository
* a blog collection
* a static FAQ system

The KB is considered:

* the foundation of retrieval quality
* the foundation of grounding quality
* the foundation of AI response reliability

Therefore:
knowledge architecture is treated as a core engineering discipline within the system.