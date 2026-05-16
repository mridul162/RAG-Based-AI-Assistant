"""
rag_generator.py

Purpose:
--------
Generate grounded multilingual answers using:
- user query
- retrieved semantic context
- OpenAI API

Architecture Philosophy:
------------------------
Retrieval-grounded generation.
Simple orchestration.
Hallucination reduction first.
"""

import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass
from typing import List

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------
# RESPONSE MODEL
# ---------------------------------------------------------

@dataclass
class GenerationResponse:

    query: str

    answer: str

    retrieval_context: str

    prompt: str


# ---------------------------------------------------------
# RAG GENERATOR
# ---------------------------------------------------------

class RAGGenerator:
    """
    Retrieval-grounded OpenAI generator.
    """

    # -----------------------------------------------------

    def __init__(
        self,
        model_name: str = "gpt-4.1-mini",
    ):

        self.model_name = model_name

        self.client = OpenAI(

            api_key=os.getenv(
                "OPENAI_API_KEY"
            )
        )

    # -----------------------------------------------------

    def generate(
        self,
        query: str,
        retrieval_context: str,
    ) -> GenerationResponse:
        """
        Main RAG generation flow.
        """

        prompt = self._build_prompt(

            query=query,

            retrieval_context=(
                retrieval_context
            ),
        )

        answer = self._generate_answer(
            prompt
        )

        return GenerationResponse(

            query=query,

            answer=answer,

            retrieval_context=(
                retrieval_context
            ),

            prompt=prompt,
        )

    # -----------------------------------------------------

    def _build_prompt(
        self,
        query: str,
        retrieval_context: str,
    ) -> str:
        """
        Build grounded RAG prompt.
        """

        return f"""
You are Hasanah Mart's multilingual AI assistant.

Your responsibilities:
- Answer ONLY using provided retrieval context
- Never invent facts
- Never hallucinate product information
- If information is unavailable, clearly say so
- Support Bangla, English, and Banglish
- Use warm, simple, customer-friendly language

IMPORTANT RULES:
- Stay grounded in retrieval context
- Do not assume missing details
- Preserve pricing accuracy
- Preserve product authenticity
- Do not generate fake health claims

==================================================
RETRIEVAL CONTEXT
==================================================

{retrieval_context}

==================================================
USER QUESTION
==================================================

{query}

==================================================
ANSWER
==================================================
""".strip()

    # -----------------------------------------------------

    def _generate_answer(
        self,
        prompt: str
    ) -> str:
        """
        Generate answer using OpenAI API.
        """

        response = (
            self.client.chat.completions.create(

                model=self.model_name,

                messages=[

                    {
                        "role": "system",

                        "content": (
                            "You are a retrieval-grounded "
                            "AI assistant for Hasanah Mart."
                        ),
                    },

                    {
                        "role": "user",

                        "content": prompt,
                    }
                ],

                temperature=0.2,
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

    # -----------------------------------------------------

    def print_response(
        self,
        response: GenerationResponse
    ):
        """
        Pretty-print response.
        """

        print("\n" + "=" * 70)
        print("RAG GENERATION RESPONSE")
        print("=" * 70)

        print(f"\nQuery:\n")

        print(response.query)

        print("\n" + "-" * 70)

        print("ANSWER")

        print("-" * 70)

        print(response.answer)

    # -----------------------------------------------------

    def print_prompt(
        self,
        response: GenerationResponse
    ):
        """
        Debug final prompt.
        """

        print("\n" + "=" * 70)
        print("FINAL RAG PROMPT")
        print("=" * 70)

        print(response.prompt)


# ---------------------------------------------------------
# SIMPLE TEST EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_context = """
[Retrieved Chunk #1]

Score:
0.8221

Metadata:
{
    "product_id": "kholisha_honey",
    "source_file": "benefits.md"
}

Content:
Raw Sundarbans Kholisha Flower Honey
contains natural antioxidants and enzymes.

--------------------------------------------------

[Retrieved Chunk #2]

Score:
0.7811

Metadata:
{
    "product_id": "kholisha_honey",
    "source_file": "pricing.md"
}

Content:
500g jar price is ৳600.
"""

    query = (
        "খলিশা ফুলের মধুর উপকারিতা কি?"
    )

    generator = RAGGenerator(

        model_name="gpt-4.1-mini"
    )

    response = generator.generate(

        query=query,

        retrieval_context=(
            sample_context
        ),
    )

    generator.print_response(
        response
    )

    # Optional:
    # generator.print_prompt(response)