"""
rag_service.py

Purpose:
--------
Main orchestration layer for the Hasanah Mart
multilingual RAG assistant.

Responsibilities:
-----------------
- Execute retrieval pipeline
- Execute grounded generation
- Format API responses
- Provide retrieval observability
- Measure pipeline timings

Architecture Philosophy:
------------------------
Thin orchestration layer.
Modular retrieval + generation.
Observable production-style pipeline.
"""

import time

from api.core.logging import (
    get_logger
)

from api.core.config import (
    settings
)

# ---------------------------------------------------------
# RETRIEVAL
# ---------------------------------------------------------

from retrieval.retriever import (
    SemanticRetriever
)

# ---------------------------------------------------------
# GENERATION
# ---------------------------------------------------------

from generation.rag_generator import (
    RAGGenerator
)

# ---------------------------------------------------------
# EMBEDDINGS
# ---------------------------------------------------------

from ingestion.embedders.bge_embedder import (
    BGEEmbedder
)

# ---------------------------------------------------------
# VECTOR STORE
# ---------------------------------------------------------

from ingestion.vectorstores.faiss_store import (
    FAISSStore
)


# ---------------------------------------------------------
# LOGGER
# ---------------------------------------------------------

logger = get_logger(__name__)


# ---------------------------------------------------------
# RAG SERVICE
# ---------------------------------------------------------

class RAGService:

    """
    Main multilingual RAG pipeline service.
    """

    # -----------------------------------------------------
    # INITIALIZATION
    # -----------------------------------------------------

    def __init__(self):

        logger.info(
            "Initializing RAG service..."
        )

        # -------------------------------------------------
        # EMBEDDER
        # -------------------------------------------------

        self.embedder = BGEEmbedder(

            model_name=(
                settings.embedding_model
            )
        )

        logger.info(
            "Embedding model loaded."
        )

        # -------------------------------------------------
        # VECTOR STORE
        # -------------------------------------------------

        self.vector_store = FAISSStore(

            embedding_dimension=(
                settings.embedding_dimension
            )
        )

        self.vector_store.load(

            index_path=(
                settings.faiss_index_path
            ),

            metadata_path=(
                settings.faiss_metadata_path
            ),
        )

        logger.info(
            "FAISS index loaded successfully."
        )

        # -------------------------------------------------
        # RETRIEVER
        # -------------------------------------------------

        self.retriever = SemanticRetriever(

            embedder=self.embedder,

            vector_store=self.vector_store,
        )

        logger.info(
            "Semantic retriever initialized."
        )

        # -------------------------------------------------
        # GENERATOR
        # -------------------------------------------------

        self.generator = RAGGenerator(

            model_name=(
                settings.chat_model
            )
        )

        logger.info(
            "RAG generator initialized."
        )

    # -----------------------------------------------------
    # MAIN RAG PIPELINE
    # -----------------------------------------------------

    def ask(
        self,
        query: str,
        top_k: int = 5,
        include_sources: bool = True,
    ):

        logger.info(
            f"Received query: {query}"
        )

        total_start_time = (
            time.perf_counter()
        )

        try:

            # -------------------------------------------------
            # RETRIEVAL
            # -------------------------------------------------

            logger.info(
                "Retrieving relevant chunks..."
            )

            retrieval_start = (
                time.perf_counter()
            )

            retrieval_response = (

                self.retriever.retrieve(

                    query=query,

                    top_k=top_k,
                )
            )

            retrieval_time = (

                time.perf_counter()

                - retrieval_start
            )

            logger.info(

                f"Retrieved "

                f"{len(retrieval_response.results)} "

                f"chunks in "

                f"{retrieval_time:.3f}s."
            )

            # -------------------------------------------------
            # GENERATION
            # -------------------------------------------------

            logger.info(
                "Generating grounded answer..."
            )

            generation_start = (
                time.perf_counter()
            )

            generation_response = (

                self.generator.generate(

                    query=query,

                    retrieval_context=(

                        retrieval_response
                        .retrieval_context
                    ),
                )
            )

            generation_time = (

                time.perf_counter()

                - generation_start
            )

            logger.info(

                f"Answer generated in "

                f"{generation_time:.3f}s."
            )

            # -------------------------------------------------
            # FORMAT SOURCES
            # -------------------------------------------------

            sources = []

            if include_sources:

                for result in (
                    retrieval_response.results
                ):

                    sources.append({

                        "chunk_id": (
                            result.chunk_id
                        ),

                        "score": round(
                            result.score,
                            4
                        ),

                        "metadata": (
                            result.metadata
                        ),

                        "preview": (
                            result.text[:300]
                        ),
                    })

            # -------------------------------------------------
            # FINAL RESPONSE
            # -------------------------------------------------

            response = {

                "query": query,

                "answer": (
                    generation_response.answer
                ),

                "sources": sources,
            }

            total_time = (

                time.perf_counter()

                - total_start_time
            )

            logger.info(

                f"Full RAG pipeline completed "

                f"in {total_time:.3f}s."
            )

            return response

        # -----------------------------------------------------
        # ERROR HANDLING
        # -----------------------------------------------------

        except Exception:

            logger.exception(
                "Error occurred inside RAG pipeline."
            )

            raise