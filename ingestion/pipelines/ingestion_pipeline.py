"""
ingestion_pipeline.py

Purpose:
--------
Main orchestration pipeline for the current ingestion phase.

Current Pipeline Scope:
-----------------------
1. Load markdown documents
2. Load product metadata
3. Validate KB structure
4. Print ingestion summary

This pipeline DOES NOT yet:
---------------------------
- parse markdown
- normalize text
- chunk documents
- generate embeddings
- build vector indexes

Those stages will be added incrementally later.

Architecture Philosophy:
------------------------
- simple
- observable
- modular
- incremental
- retrieval-first
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
from collections import Counter
import ingestion.loaders
import ingestion.validators

# ---------------------------------------------------------
# IMPORT LOADERS
# ---------------------------------------------------------

from ingestion.loaders.markdown_loader import (
    MarkdownLoader
)

from ingestion.loaders.product_metadata_loader import (
    ProductMetadataLoader
)

# ---------------------------------------------------------
# IMPORT VALIDATOR
# ---------------------------------------------------------

from ingestion.validators.kb_validator import (
    KBValidator,
    print_validation_report
)


# ---------------------------------------------------------
# INGESTION PIPELINE
# ---------------------------------------------------------

class IngestionPipeline:
    """
    Main ingestion pipeline orchestrator.
    """

    def __init__(
        self,
        kb_root: str,
    ):

        self.kb_root = Path(kb_root)

        # -------------------------------------------------
        # Initialize components
        # -------------------------------------------------

        self.markdown_loader = MarkdownLoader(
            kb_root=str(self.kb_root)
        )

        self.metadata_loader = ProductMetadataLoader(
            kb_root=str(self.kb_root)
        )

        self.validator = KBValidator(
            kb_root=str(self.kb_root)
        )

    # -----------------------------------------------------

    def run(self):
        """
        Execute current ingestion pipeline.
        """

        self._print_pipeline_header()

        # -------------------------------------------------
        # STEP 1 — VALIDATION
        # -------------------------------------------------

        print("\n[STEP 1] Validating Knowledge Base...\n")

        validation_report = self.validator.validate()

        print_validation_report(
            validation_report
        )

        # -------------------------------------------------
        # Stop pipeline if KB invalid
        # -------------------------------------------------

        if not validation_report.valid:

            print("\n[PIPELINE STOPPED]")
            print(
                "Knowledge base contains validation errors."
            )

            return

        # -------------------------------------------------
        # STEP 2 — LOAD MARKDOWN DOCUMENTS
        # -------------------------------------------------

        print("\n[STEP 2] Loading Markdown Documents...\n")

        documents = self.markdown_loader.load()

        print(
            f"Loaded {len(documents)} markdown documents."
        )

        # -------------------------------------------------
        # STEP 3 — LOAD PRODUCT METADATA
        # -------------------------------------------------

        print("\n[STEP 3] Loading Product Metadata...\n")

        metadata_objects = self.metadata_loader.load()

        print(
            f"Loaded {len(metadata_objects)} metadata files."
        )

        # -------------------------------------------------
        # STEP 4 — INGESTION SUMMARY
        # -------------------------------------------------

        self._print_ingestion_summary(
            documents,
            metadata_objects,
        )

        print("\n[PIPELINE COMPLETED SUCCESSFULLY]")

    # -----------------------------------------------------

    def _print_pipeline_header(self):

        print("\n" + "=" * 70)
        print("HASANAH MART RAG INGESTION PIPELINE")
        print("=" * 70)

        print(f"\nKnowledge Base Root:")
        print(f"{self.kb_root}")

    # -----------------------------------------------------

    def _print_ingestion_summary(
        self,
        documents,
        metadata_objects,
    ):

        print("\n" + "=" * 70)
        print("INGESTION SUMMARY")
        print("=" * 70)

        # -------------------------------------------------
        # Document Statistics
        # -------------------------------------------------

        print("\nDOCUMENT STATISTICS")
        print("-" * 70)

        print(f"Total Documents : {len(documents)}")

        # -------------------------------------------------
        # Category Distribution
        # -------------------------------------------------

        category_counter = Counter(
            doc.category
            for doc in documents
        )

        print("\nDocuments Per Category:")

        for category, count in sorted(
            category_counter.items()
        ):

            print(f"  - {category}: {count}")

        # -------------------------------------------------
        # File Type Distribution
        # -------------------------------------------------

        file_type_counter = Counter(
            doc.file_type
            for doc in documents
        )

        print("\nDocuments Per File Type:")

        for file_type, count in sorted(
            file_type_counter.items()
        ):

            print(f"  - {file_type}: {count}")

        # -------------------------------------------------
        # Metadata Statistics
        # -------------------------------------------------

        print("\nMETADATA STATISTICS")
        print("-" * 70)

        print(
            f"Total Product Metadata Files : "
            f"{len(metadata_objects)}"
        )

        # -------------------------------------------------
        # Product Coverage
        # -------------------------------------------------

        document_product_ids = set(
            doc.product_id
            for doc in documents
        )

        metadata_product_ids = set(
            metadata.product_id
            for metadata in metadata_objects
        )

        missing_metadata = (
            document_product_ids -
            metadata_product_ids
        )

        if missing_metadata:

            print("\nProducts Missing Metadata:")

            for product_id in sorted(
                missing_metadata
            ):

                print(f"  - {product_id}")

        else:

            print(
                "\nAll products have metadata coverage."
            )

        # -------------------------------------------------
        # Sample Document Preview
        # -------------------------------------------------

        if documents:

            sample = documents[0]

            print("\nSAMPLE DOCUMENT")
            print("-" * 70)

            print(f"Product ID : {sample.product_id}")
            print(f"Category   : {sample.category}")
            print(f"File Type  : {sample.file_type}")
            print(f"Path       : {sample.path}")

            preview = sample.content[:300]

            print("\nContent Preview:\n")

            print(preview)


# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":

    pipeline = IngestionPipeline(

        # Recommended KB root:
        # knowledge_base/catalog/products

        kb_root="knowledge_base/catalog/products"
    )

    pipeline.run()