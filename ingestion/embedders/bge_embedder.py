"""
bge_embedder.py

Purpose:
--------
Generate multilingual semantic embeddings for
retrieval-ready chunks using BAAI/bge-m3.

Responsibilities:
-----------------
- Load embedding model
- Generate embeddings for chunks
- Preserve chunk metadata
- Produce embedding-ready objects
- Persist embedding artifacts

This embedder DOES NOT:
-----------------------
- build vector indexes
- rerank retrieval
- cache embeddings
- batch optimize aggressively
- detect incremental updates

Architecture Philosophy:
------------------------
Correctness first.
Observability first.
Optimization later.
"""

import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List

from sentence_transformers import (
    SentenceTransformer
)


# ---------------------------------------------------------
# EMBEDDING MODEL
# ---------------------------------------------------------

@dataclass
class EmbeddedChunk:
    """
    Retrieval-ready embedded chunk.
    """

    chunk_id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]


# ---------------------------------------------------------
# BGE EMBEDDER
# ---------------------------------------------------------

class BGEEmbedder:
    """
    Multilingual semantic embedder using BAAI/bge-m3.
    """

    DEFAULT_MODEL = "BAAI/bge-m3"

    # -----------------------------------------------------

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
    ):

        print("\nLoading embedding model...")

        self.model = SentenceTransformer(
            model_name
        )

        print(
            f"Loaded model: {model_name}"
        )

    # -----------------------------------------------------

    def embed_chunks(
        self,
        chunks,
    ) -> List[EmbeddedChunk]:
        """
        Generate embeddings for chunks.
        """

        embedded_chunks = []

        for i, chunk in enumerate(chunks, start=1):

            print(
                f"Embedding chunk "
                f"{i}/{len(chunks)}"
            )

            embedding = self._generate_embedding(
                chunk.text
            )

            embedded_chunk = EmbeddedChunk(

                chunk_id=chunk.chunk_id,

                text=chunk.text,

                embedding=embedding,

                metadata=chunk.metadata,
            )

            embedded_chunks.append(
                embedded_chunk
            )

        return embedded_chunks

    # -----------------------------------------------------

    def _generate_embedding(
        self,
        text: str
    ) -> List[float]:
        """
        Generate embedding vector.
        """

        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    # -----------------------------------------------------

    def persist_embeddings(
        self,
        embedded_chunks,
        output_path: str,
    ):
        """
        Persist embeddings as UTF-8 JSON.
        """

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        artifact_data = []

        for chunk in embedded_chunks:

            artifact_data.append({

                "chunk_id": (
                    chunk.chunk_id
                ),

                "text": (
                    chunk.text
                ),

                "embedding": (
                    chunk.embedding
                ),

                "metadata": (
                    chunk.metadata
                ),
            })

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                artifact_data,
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(
            f"\nEmbeddings written to:"
        )

        print(output_path)


# ---------------------------------------------------------
# SIMPLE TEST EXECUTION
# ---------------------------------------------------------

# if __name__ == "__main__":

#     from dataclasses import dataclass
#     from typing import Dict, Any

#     # -----------------------------------------------------
#     # Mock Chunk Model
#     # -----------------------------------------------------

#     @dataclass
#     class Chunk:

#         chunk_id: str
#         text: str
#         metadata: Dict[str, Any]

#     # -----------------------------------------------------
#     # Sample Chunks
#     # -----------------------------------------------------

#     chunks = [

#         Chunk(

#             chunk_id="chunk_001",

#             text="""
#             Sundarbans Kholisha Flower Honey
#             is naturally sourced from the
#             mangrove forests of Bangladesh.
#             """,

#             metadata={

#                 "product_id": (
#                     "kholisha_honey"
#                 ),

#                 "category": "honey",

#                 "source_file": (
#                     "overview.md"
#                 ),
#             }
#         ),

#         Chunk(

#             chunk_id="chunk_002",

#             text="""
#             খাঁটি কাঁচা মধু প্রাকৃতিক
#             অ্যান্টিঅক্সিডেন্টে সমৃদ্ধ।
#             """,

#             metadata={

#                 "product_id": (
#                     "kholisha_honey"
#                 ),

#                 "category": "honey",

#                 "source_file": (
#                     "benefits.md"
#                 ),
#             }
#         )
#     ]

#     # -----------------------------------------------------
#     # Embed Chunks
#     # -----------------------------------------------------

#     embedder = BGEEmbedder()

#     embedded_chunks = embedder.embed_chunks(
#         chunks
#     )

#     # -----------------------------------------------------
#     # Persist Embeddings
#     # -----------------------------------------------------

#     embedder.persist_embeddings(

#         embedded_chunks=embedded_chunks,

#         output_path=(
#             "artifacts/embeddings/"
#             "sample_embeddings.json"
#         )
#     )

#     # -----------------------------------------------------
#     # Preview
#     # -----------------------------------------------------

#     print("\n" + "=" * 70)
#     print("EMBEDDING SUMMARY")
#     print("=" * 70)

#     print(
#         f"\nEmbedded Chunks: "
#         f"{len(embedded_chunks)}"
#     )

#     sample = embedded_chunks[0]

#     print("\nSample Chunk:")

#     print(
#         f"Chunk ID: {sample.chunk_id}"
#     )

#     print(
#         f"Embedding Dimensions: "
#         f"{len(sample.embedding)}"
#     )

#     print("\nMetadata:")

#     print(sample.metadata)