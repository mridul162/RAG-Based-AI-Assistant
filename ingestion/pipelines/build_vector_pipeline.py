"""
build_vector_pipeline.py

Purpose:
--------
Complete ingestion pipeline integration for the
Hasanah Mart multilingual RAG system.

Pipeline:
---------
1. Validate KB
2. Load markdown documents
3. Load structured metadata
4. Parse markdown documents
5. Chunk parsed sections
6. Generate OpenAI embeddings
7. Build FAISS vector store
8. Save vector artifacts

Architecture:
--------------
KB Validator
    ↓
Markdown Loader
Metadata Loader
    ↓
Markdown Parser
    ↓
Semantic Chunker
    ↓
OpenAI Embedder
    ↓
FAISS Vector Store
"""

import sys

sys.stdout.reconfigure(
    encoding="utf-8"
)

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from api.core.config import (
    settings
)

from api.core.logging import (
    get_logger,
    setup_logging
)

from ingestion.validators.kb_validator import (
    KBValidator,
    print_validation_report
)

from ingestion.loaders.markdown_loader import (
    MarkdownLoader
)

from ingestion.loaders.product_metadata_loader import (
    ProductMetadataLoader
)

from ingestion.parsers.markdown_parser import (
    MarkdownParser
)

from ingestion.chunkers.semantic_chunker import (
    SemanticChunker
)

from ingestion.embedders.openai_embedder import (
    OpenAIEmbedder
)

from ingestion.vectorstores.faiss_store import (
    FAISSStore
)


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

setup_logging()

logger = get_logger(__name__)


# ---------------------------------------------------------
# EMBEDDED CHUNK MODEL
# ---------------------------------------------------------

@dataclass
class EmbeddedChunk:

    chunk_id: str

    text: str

    embedding: List[float]

    metadata: Dict[str, Any]


# ---------------------------------------------------------
# VECTOR PIPELINE
# ---------------------------------------------------------

class VectorPipeline:

    """
    End-to-end ingestion pipeline.
    """

    # -----------------------------------------------------

    def __init__(self):

        logger.info(
            "Initializing vector pipeline..."
        )

        # -------------------------------------------------
        # KB ROOT
        # -------------------------------------------------

        self.kb_root = (
            settings.kb_root
        )

        # -------------------------------------------------
        # VALIDATOR
        # -------------------------------------------------

        self.validator = KBValidator(
            kb_root=self.kb_root
        )

        # -------------------------------------------------
        # LOADERS
        # -------------------------------------------------

        self.markdown_loader = (
            MarkdownLoader(
                kb_root=self.kb_root
            )
        )

        self.metadata_loader = (
            ProductMetadataLoader(
                kb_root=self.kb_root
            )
        )

        # -------------------------------------------------
        # PARSER
        # -------------------------------------------------

        self.parser = MarkdownParser()

        # -------------------------------------------------
        # CHUNKER
        # -------------------------------------------------

        self.chunker = SemanticChunker(

            target_size=(
                settings.chunk_size
            ),

            overlap_size=(
                settings.chunk_overlap
            )
        )

        # -------------------------------------------------
        # EMBEDDER
        # -------------------------------------------------

        self.embedder = (
            OpenAIEmbedder()
        )

        logger.info(
            "OpenAI embedder initialized."
        )

    # -----------------------------------------------------

    def run(self):

        logger.info(
            "Starting ingestion pipeline..."
        )

        # =================================================
        # STEP 1: VALIDATE KB
        # =================================================

        logger.info(
            "Validating knowledge base..."
        )

        validation_report = (
            self.validator.validate()
        )

        print_validation_report(
            validation_report
        )

        if not validation_report.valid:

            raise ValueError(
                "Knowledge base validation failed."
            )

        logger.info(
            "Knowledge base validation passed."
        )

        # =================================================
        # STEP 2: LOAD MARKDOWN DOCUMENTS
        # =================================================

        logger.info(
            "Loading markdown documents..."
        )

        markdown_documents = (
            self.markdown_loader.load()
        )

        logger.info(
            f"Loaded "
            f"{len(markdown_documents)} "
            f"markdown documents."
        )

        # =================================================
        # STEP 3: LOAD PRODUCT METADATA
        # =================================================

        logger.info(
            "Loading product metadata..."
        )

        product_metadata = (
            self.metadata_loader.load()
        )

        logger.info(
            f"Loaded "
            f"{len(product_metadata)} "
            f"metadata entries."
        )

        # =================================================
        # STEP 4: CREATE METADATA MAP
        # =================================================

        metadata_map = {}

        for metadata in product_metadata:

            metadata_map[
                metadata.product_id
            ] = metadata

        # =================================================
        # STEP 5: PARSE MARKDOWN
        # =================================================

        logger.info(
            "Parsing markdown documents..."
        )

        parsed_sections = []

        for document in markdown_documents:

            sections = (
                self.parser.parse(
                    document.content
                )
            )

            for section in sections:

                parsed_sections.append({

                    "document": document,

                    "section": section
                })

        logger.info(
            f"Parsed "
            f"{len(parsed_sections)} "
            f"sections."
        )

        # =================================================
        # STEP 6: CHUNK SECTIONS
        # =================================================

        logger.info(
            "Chunking parsed sections..."
        )

        chunks = []

        for item in parsed_sections:

            document = item["document"]

            section = item["section"]

            product_id = getattr(
                document,
                "product_id",
                None
            )

            metadata = (
                metadata_map.get(
                    product_id
                )
            )

            section_chunks = (
                self.chunker.chunk_sections(

                    sections=[section],

                    base_metadata={

                        "product_id": getattr(
                            metadata,
                            "product_id",
                            None
                        ),

                        "product_name": getattr(
                            metadata,
                            "name",
                            None
                        ),

                        "category": getattr(
                            metadata,
                            "category",
                            None
                        ),

                        "source_file": getattr(
                            document,
                            "source_path",
                            None
                        ),
                    }
                )
            )

            chunks.extend(
                section_chunks
            )

        logger.info(
            f"Generated "
            f"{len(chunks)} chunks."
        )

        if not chunks:

            raise ValueError(
                "No chunks generated."
            )

        # =================================================
        # STEP 7: GENERATE EMBEDDINGS
        # =================================================

        logger.info(
            "Generating embeddings..."
        )

        chunk_texts = [

            chunk.text

            for chunk in chunks
        ]

        embeddings = (
            self.embedder.embed_texts(
                chunk_texts
            )
        )

        logger.info(
            "Embeddings generated successfully."
        )

        logger.info(
            f"Embedding dimension: "
            f"{len(embeddings[0])}"
        )

        # =================================================
        # STEP 8: BUILD EMBEDDED CHUNKS
        # =================================================

        logger.info(
            "Building embedded chunks..."
        )

        embedded_chunks = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            embedded_chunk = (
                EmbeddedChunk(

                    chunk_id=(
                        chunk.chunk_id
                    ),

                    text=chunk.text,

                    embedding=embedding,

                    metadata={
                        "source": getattr(
                            chunk,
                            "source",
                            None
                        ),

                        "product_id": getattr(
                            chunk,
                            "product_id",
                            None
                        ),

                        "section_type": getattr(
                            chunk,
                            "section_type",
                            None
                        ),

                        "heading": getattr(
                            chunk,
                            "heading",
                            None
                        ),
                    }
                )
            )

            embedded_chunks.append(
                embedded_chunk
            )

        logger.info(
            f"Created "
            f"{len(embedded_chunks)} "
            f"embedded chunks."
        )

        # =================================================
        # STEP 9: BUILD VECTOR STORE
        # =================================================

        logger.info(
            "Building FAISS vector store..."
        )

        vector_store = FAISSStore(
            embedding_dimension=(
                len(embeddings[0])
            )
        )

        vector_store.add_embeddings(
            embedded_chunks
        )

        logger.info(
            f"Indexed "
            f"{vector_store.total_vectors()} "
            f"vectors."
        )

        # =================================================
        # STEP 10: SAVE ARTIFACTS
        # =================================================

        logger.info(
            "Saving vector database..."
        )

        vector_store.save(

            index_path=(
                settings.faiss_index_path
            ),

            metadata_path=(
                settings.metadata_path
            )
        )

        logger.info(
            "Vector database saved successfully."
        )

        logger.info(
            "Pipeline completed successfully."
        )


# ---------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------

if __name__ == "__main__":

    pipeline = VectorPipeline()

    pipeline.run()