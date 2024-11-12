from __future__ import annotations

import os
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing import List


class VectorDBManager:
    def __init__(
        self, vector_db_dir: Path, database_name: str, embeddings: OpenAIEmbeddings
    ):
        self.vector_db_dir = vector_db_dir
        self.database_name = database_name
        self.embeddings = embeddings

        # Define in-memory metadata schema to match document metadata
        self.metadata_schema = {
            "type": ["research_article"],  # From ResearchArticle
            "document_type": [
                "scientific_research",
                "team_roster",
            ],  # From both classes
            "used_for": [
                "Scientific research on water quality and salinity",
                "Queries about the SaltCast team",
                "Queries on 1 or more saltcast team member(s)",
            ],
            "topics": [
                "salinity",
                "climate change",
                "water quality",
                "HABs",
                "drinking water",
                "chesapeake bay",
                "research methods",
            ],
            "relevance": [
                "water suppliers",
                "coastal communities",
                "researchers and scientists",
                "policy makers",
                "agricultural users",
                "general scientific audience",
            ],
        }
        self.database = self.load_database()

    def load_database(self) -> FAISS:
        """Load the FAISS database and attach metadata schema."""

        try:
            db = FAISS.load_local(
                self.vector_db_dir,
                self.embeddings,
                self.database_name,
                allow_dangerous_deserialization=True,
            )
            # Attach metadata schema to loaded database
            db.metadata_schema = self.metadata_schema
            return db
        except Exception as e:
            raise RuntimeError(f"Failed to load database: {e}")

    def get_relevant_docs(
        self,
        *,
        prompt: str,
        max_docs: Optional[int] = 4,  # 4 is langchain default
        score_threshold: Optional[float] = 0.5,
    ) -> List[str]:
        """
        Retrieve relevant documents using metadata filtering and relevance scores.

        Args:
            prompt (str): The prompt to search for relevant documents.
            max_docs (int): Maximum number of documents to return.
            score_threshold (float): Minimum relevance score (0-1) to consider relevant.

        Returns:
            List[str]: A list of relevant document contents.
        """
        try:
            prompt_lower = prompt.lower()
            metadata_filter = {}

            # Build metadata filter based on schema
            for field, values in self.metadata_schema.items():
                for value in values:
                    if value.lower() in prompt_lower:
                        metadata_filter[field] = value

            # Search with metadata filter and get relevance scores
            docs_and_scores = self.database.similarity_search_with_relevance_scores(
                prompt, k=max_docs, filter=metadata_filter if metadata_filter else None
            )

            # Filter by relevance score
            relevant_docs = [
                doc.page_content
                for doc, score in docs_and_scores
                if score >= score_threshold
            ][:max_docs]

            return relevant_docs
        except Exception as e:
            print(f"Warning: Failed to retrieve relevant documents: {e}")
            return []
