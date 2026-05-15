# CHUNKING_STRATEGY.md

# Hasanah Mart AI Assistant — Chunking Strategy

---

# 1. Purpose

This document defines the chunking architecture and chunk generation rules for the Hasanah Mart multilingual RAG system.

Chunking is a foundational retrieval engineering component.

Chunk quality directly affects:

* retrieval precision
* grounding fidelity
* hallucination rate
* multilingual retrieval quality
* reranking quality
* token efficiency

This document establishes:

* chunking philosophy
* segmentation rules
* semantic boundaries
* metadata attachment rules
* incremental re-indexing strategy
* multilingual chunking considerations

---

# 2. Chunking Philosophy

The system uses:

```text id="7jlwmu"
Semantic + Heading-Aware Hybrid Chunking
```

NOT:

* naive fixed-size chunking
* purely character-based chunking
* arbitrary token slicing

Chunking is designed to preserve:

* semantic coherence
* retrieval relevance
* contextual independence

---

# 3. Core Chunking Principles

---

# 3.1 Semantic Isolation

Each chunk should ideally represent:

* one semantic intent cluster
* one coherent retrieval topic

Example:

* benefits
* sourcing
* storage
* warnings

should remain semantically isolated whenever possible.

---

# 3.2 Contextual Independence

A chunk should remain understandable even when retrieved independently.

Chunks should avoid:

* excessive dependency on previous chunks
* unresolved references
* ambiguous pronouns
* missing contextual anchors

---

# 3.3 Retrieval-Oriented Segmentation

Chunk boundaries should optimize:

* semantic retrieval quality
* grounding precision
* reranking quality

NOT:

* document readability alone

---

# 3.4 Modular Chunk Evolution

The chunking system must support:

* incremental updates
* partial re-indexing
* localized re-embedding

without requiring:

* full KB regeneration

---

# 4. Chunking Strategy

---

# 4.1 Chunking Method

The system uses a hybrid strategy:

```text id="4jlwmd"
Heading-Aware Segmentation
        +
Semantic Boundary Segmentation
        +
Token-Limit Enforcement
```

---

# 4.2 Chunk Boundary Priority

Chunk boundaries should prioritize:

1. Markdown headings
2. FAQ question boundaries
3. List boundaries
4. Paragraph semantic shifts
5. Token limits

---

# 4.3 Preferred Chunk Structure

Preferred chunk characteristics:

* semantically focused
* retrieval-friendly
* contextually understandable
* multilingual-safe
* low semantic noise

---

# 5. Chunk Size Rules

---

# 5.1 Recommended Chunk Size

Preferred range:

```text id="1jlwmg"
300–700 tokens
```

Hard upper limit:

```text id="3jlwmt"
900 tokens
```

Reason:

* preserves semantic richness
* reduces retrieval fragmentation
* avoids excessive context pollution

---

# 5.2 Minimum Chunk Size

Preferred minimum:

```text id="6jlwmb"
80–120 tokens
```

Very small chunks may:

* reduce retrieval quality
* lose semantic context
* increase vector noise

---

# 6. Chunk Overlap Strategy

---

# 6.1 Overlap Size

Recommended overlap:

```text id="8jlwmu"
10–15%
```

---

# 6.2 Overlap Purpose

Overlap exists to:

* preserve semantic continuity
* reduce boundary fragmentation
* improve contextual transitions

---

# 6.3 Overlap Restrictions

Avoid:

* excessive duplication
* repeated semantic noise
* large overlap windows

---

# 7. Semantic Boundary Rules

---

# 7.1 Never Mix Unrelated Domains

Avoid chunks containing:

* pricing + benefits
* warnings + testimonials
* recipes + sourcing

Each chunk should remain:

* semantically narrow
* retrieval-focused

---

# 7.2 FAQ Chunking

Each FAQ question-answer pair should ideally become:

* its own retrieval chunk

Reason:
FAQ retrieval is highly intent-driven.

---

# 7.3 List Handling

Short lists may remain within parent chunks.

Large lists should become:

* separate semantic chunks

---

# 7.4 Table Handling

Tables should:

* remain structurally preserved
* avoid row fragmentation

especially:

* nutrition data
* comparison data
* pricing data

---

# 8. Heading-Aware Chunking

---

# 8.1 Markdown Heading Priority

Chunking should respect:

* H1
* H2
* H3

as semantic segmentation boundaries.

---

# 8.2 Preferred Strategy

Example:

```text id="5jlwmy"
# Benefits
    ↓
Chunk Group

## Immunity
    ↓
Subchunk

## Digestion
    ↓
Subchunk
```

---

# 9. Multilingual Chunking Strategy

---

# 9.1 Supported Languages

The system supports:

* Bengali
* English
* Banglish
* Mixed-language content

---

# 9.2 Multilingual Preservation

Chunking should preserve:

* native script
* transliterated terms
* mixed-language phrasing

Avoid:

* splitting multilingual phrase groups

---

# 9.3 Alias Preservation

Aliases and multilingual variants should remain attached to:

* product metadata
* retrieval metadata

NOT fragmented separately.

---

# 10. Metadata Attachment Rules

---

# 10.1 Every Chunk Must Include Metadata

Required metadata:

```json id="9jlwme"
{
  "chunk_id": "",
  "product_id": "",
  "category": "",
  "knowledge_type": "",
  "source_file": "",
  "chunk_index": "",
  "language": "",
  "visibility": "",
  "semantic_domain": ""
}
```

---

# 10.2 Metadata Consistency

Metadata must remain:

* deterministic
* reproducible
* stable across re-indexing

---

# 11. Chunk ID Strategy

---

# 11.1 Chunk ID Format

Recommended structure:

```text id="2jlwms"
product_id__knowledge_type__chunk_index
```

Example:

```text id="5jlwmp"
sundarbans_kholisha_honey__benefits__001
```

---

# 11.2 Chunk ID Stability

Chunk IDs should remain stable whenever possible.

This improves:

* incremental updates
* observability
* retrieval debugging

---

# 12. Incremental Re-Chunking Strategy

---

# 12.1 File-Level Reprocessing

Only modified files should trigger:

* re-chunking
* re-embedding
* vector replacement

The entire KB should NOT be regenerated for:

* localized content changes

---

# 12.2 Chunk Replacement Strategy

When a file changes:

1. old chunks removed
2. file re-chunked
3. new embeddings generated
4. vector index updated

---

# 13. Empty File Handling

---

# 13.1 Empty Files

Empty files should:

* remain valid
* generate zero chunks
* produce zero embeddings

This supports:

* gradual KB enrichment

---

# 13.2 Placeholder Restrictions

Avoid placeholder text like:

* TODO
* Coming soon
* Add later

because these may:

* pollute embeddings
* degrade retrieval quality

---

# 14. Chunk Validation Rules

---

# 14.1 Validation Checks

Future chunk validation should detect:

* empty chunks
* duplicate chunks
* oversized chunks
* malformed markdown
* metadata inconsistencies

---

# 14.2 Semantic Validation

Future evaluation may include:

* semantic coherence scoring
* overlap quality analysis
* retrieval effectiveness testing

---

# 15. Anti-Patterns

Avoid:

* giant chunks
* cross-domain chunks
* excessive overlap
* sentence fragmentation
* duplicated semantic regions
* isolated orphan sentences

---

# 16. Retrieval Assumptions

The chunking system is designed to support future:

* metadata filtering
* reranking
* hybrid retrieval
* multilingual retrieval
* retrieval observability
* retrieval analytics

without requiring:

* full chunking redesign

---

# 17. Long-Term Evolution

The current chunking architecture is intentionally:

* modular
* deterministic
* inspectable
* reproducible

Future evolution may include:

* semantic graph chunking
* adaptive chunk sizing
* query-aware chunking
* hierarchical retrieval
* dynamic reranking

The current design should not block these future transitions.

---

# 18. Architectural Summary

The Hasanah Mart chunking system is designed as:

```text id="4jlwmb"
A retrieval-first semantic chunking architecture
```

optimized for:

* multilingual retrieval
* semantic precision
* grounding fidelity
* scalable incremental indexing
* production-oriented RAG engineering.
