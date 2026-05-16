"""
retriever.py

Purpose:
--------
High-level semantic retrieval interface for the
Hasanah Mart multilingual RAG system.

Responsibilities:
-----------------
- Embed user queries
- Perform FAISS similarity search
- Return retrieval-ready results
- Provide retrieval debugging utilities
- Format retrieval context

Architecture Philosophy:
------------------------
Simple retrieval orchestration.
Transparent retrieval flow.
Debuggable semantic retrieval.
"""

import sys

sys.stdout.reconfigure(
    encoding="utf-8"
)

from dataclasses import dataclass

from typing import (
    List,
    Dict,
    Any,
)

from ingestion.embedders.openai_embedder import (
    OpenAIEmbedder
)

from ingestion.vectorstores.faiss_store import (
    FAISSStore,
    RetrievalResult,
)


# ---------------------------------------------------------
# RETRIEVAL RESPONSE MODEL
# ---------------------------------------------------------

@dataclass
class RetrievalResponse:
    """
    High-level retrieval response.
    """

    query: str

    results: List[RetrievalResult]

    retrieval_context: str


# ---------------------------------------------------------
# SEMANTIC RETRIEVER
# ---------------------------------------------------------

class SemanticRetriever:
    """
    Multilingual semantic retriever.
    """

    # -----------------------------------------------------

    def __init__(
        self,
        embedder: OpenAIEmbedder,
        vector_store: FAISSStore,
    ):

        self.embedder = embedder

        self.vector_store = vector_store

    # -----------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> RetrievalResponse:
        """
        Main retrieval pipeline.
        """

        print("\nEmbedding query...")

        query_embedding = (
            self.embedder.embed_text(
                query
            )
        )

        print(
            "Searching vector store..."
        )

        results = (
            self.vector_store.search(

                query_embedding=(
                    query_embedding
                ),

                top_k=top_k,
            )
        )

        retrieval_context = (
            self._build_context(
                results
            )
        )

        return RetrievalResponse(

            query=query,

            results=results,

            retrieval_context=(
                retrieval_context
            ),
        )

    # -----------------------------------------------------

    def _build_context(
        self,
        results: List[
            RetrievalResult
        ]
    ) -> str:
        """
        Build retrieval context string.
        """

        context_blocks = []

        for i, result in enumerate(
            results,
            start=1
        ):

            block = f"""
[Retrieved Chunk #{i}]

Score:
{result.score:.4f}

Metadata:
{result.metadata}

Content:
{result.text}
"""

            context_blocks.append(
                block.strip()
            )

        return "\n\n".join(
            context_blocks
        )

    # -----------------------------------------------------

    def print_results(
        self,
        retrieval_response: (
            RetrievalResponse
        )
    ):
        """
        Pretty-print retrieval results.
        """

        print("\n" + "=" * 70)

        print(
            "RETRIEVAL RESULTS"
        )

        print("=" * 70)

        print(
            f"\nQuery: "
            f"{retrieval_response.query}"
        )

        print(
            f"\nRetrieved Chunks: "
            f"{len(retrieval_response.results)}"
        )

        for i, result in enumerate(
            retrieval_response.results,
            start=1
        ):

            print("\n" + "-" * 70)

            print(
                f"RESULT #{i}"
            )

            print("-" * 70)

            print(
                f"Score: "
                f"{result.score:.4f}"
            )

            print(
                f"Chunk ID: "
                f"{result.chunk_id}"
            )

            print("\nMetadata:")

            for k, v in (
                result.metadata.items()
            ):

                print(f"{k}: {v}")

            print(
                "\nText Preview:"
            )

            print(
                result.text[:700]
            )


# ---------------------------------------------------------
# SIMPLE TEST EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":

    # -----------------------------------------------------
    # Sample Chunks
    # -----------------------------------------------------

    sample_chunks = [

        {
            "chunk_id": "chunk_001",

            "text": """
            Sundarbans Kholisha Flower Honey
            is naturally sourced from the
            mangrove forests of Bangladesh.
            """,

            "metadata": {
                "source_file": (
                    "overview.md"
                )
            }
        },

        {
            "chunk_id": "chunk_002",

            "text": """
            Raw honey contains natural
            antioxidants and enzymes.
            """,

            "metadata": {
                "source_file": (
                    "benefits.md"
                )
            }
        },

        {
            "chunk_id": "chunk_003",

            "text": """
            মধু ঠান্ডা ও শুকনো স্থানে
            সংরক্ষণ করা উচিত।
            """,

            "metadata": {
                "source_file": (
                    "storage.md"
                )
            }
        }
    ]

    # -----------------------------------------------------
    # Initialize Embedder
    # -----------------------------------------------------

    embedder = OpenAIEmbedder()

    # -----------------------------------------------------
    # Embedded Chunk Model
    # -----------------------------------------------------

    @dataclass
    class EmbeddedChunk:

        chunk_id: str

        text: str

        embedding: List[float]

        metadata: Dict[
            str,
            Any
        ]

    # -----------------------------------------------------
    # Generate Embedded Chunks
    # -----------------------------------------------------

    embedded_chunks = []

    for chunk in sample_chunks:

        embedding = (
            embedder.embed_text(
                chunk["text"]
            )
        )

        embedded_chunks.append(

            EmbeddedChunk(

                chunk_id=(
                    chunk["chunk_id"]
                ),

                text=chunk["text"],

                embedding=(
                    embedding
                ),

                metadata=(
                    chunk["metadata"]
                ),
            )
        )

    # -----------------------------------------------------
    # Build Vector Store
    # -----------------------------------------------------

    embedding_dimension = len(
        embedded_chunks[0]
        .embedding
    )

    vector_store = FAISSStore(
        embedding_dimension
    )

    vector_store.add_embeddings(
        embedded_chunks
    )

    # -----------------------------------------------------
    # Create Retriever
    # -----------------------------------------------------

    retriever = (
        SemanticRetriever(

            embedder=embedder,

            vector_store=(
                vector_store
            ),
        )
    )

    # -----------------------------------------------------
    # Run Retrieval Query
    # -----------------------------------------------------

    query = (
        "র মধুর উপকারিতা কী?"
    )

    response = retriever.retrieve(

        query=query,

        top_k=3,
    )

    # -----------------------------------------------------
    # Print Results
    # -----------------------------------------------------

    retriever.print_results(
        response
    )

    # -----------------------------------------------------
    # Print Retrieval Context
    # -----------------------------------------------------

    print("\n" + "=" * 70)

    print(
        "RETRIEVAL CONTEXT"
    )

    print("=" * 70)

    print(
        response.retrieval_context
    )