from pydantic import BaseModel, Field
from typing import List, Dict
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import json


class TranscriptItem(BaseModel):
    fact_or_information: str
    metadata: Dict[str, str]

    def to_document(self) -> Document:
        return Document(page_content=self.fact_or_information, metadata=self.metadata)


class TranscriptData(BaseModel):
    transcript_items: List[TranscriptItem]

    @classmethod
    def from_json_file(cls, file_path: str) -> "TranscriptData":
        with open(file_path, "r") as f:
            data = json.load(f)
            # Wrap the list in a dict with transcript_items key so that the pydantic model can be instantiated
            return cls(transcript_items=[TranscriptItem(**item) for item in data])

    def to_documents(self) -> List[Document]:
        return [item.to_document() for item in self.transcript_items]


class TeamListItem(BaseModel):
    name: str
    role: str
    priority: int
    description: str

    def to_document(self) -> Document:
        document = Document(
            page_content=(
                "Team Member:\n"
                f"Name:{self.name}\n"
                f"Role:{self.role}\n"
                f"Description:{self.description}\n"
                f"Priority (Lower is Better):{self.priority}"
            ),
            metadata={
                "name": self.name,
                "role": self.role,
                "priority": self.priority,
                "description": self.description,
                "priority_note": "Lower is Better",
                "used_for": "Queries on 1 or more saltcast team member(s)",
            },
        )
        print(f"\n\nTEAM LIST ITEM DOCUMENT:\n\n{document}\n\n")
        return document


class TeamListData(BaseModel):
    team_list_items: List[TeamListItem]

    @classmethod
    def from_csv(cls, file_path: str) -> "TeamListData":
        df = pd.read_csv(file_path)
        column_mapping = {
            "Name": "name",
            "Role": "role",
            "Priority (Lower is Better)": "priority",
            "Description": "description",
        }
        df = df.rename(columns=column_mapping)

        return cls(
            team_list_items=[TeamListItem(**row.to_dict()) for _, row in df.iterrows()]
        )

    def to_documents(self) -> List[Document]:
        # Create a single document with all team member information
        team_info = "SaltCast Team Members:\n\n"
        team_metadata = {
            "team_members": {},
            "used_for": "Queries about the SaltCast team",
            "document_type": "team_roster",
        }

        for member in self.team_list_items:
            # Add to content string
            team_info += (
                f"Name: {member.name}\n"
                f"Role: {member.role}\n"
                f"Description: {member.description}\n"
                f"Priority: {member.priority} (Lower is Better)\n"
                f"-------------------\n"
            )

            # Add to metadata
            team_metadata["team_members"][member.name] = {
                "role": member.role,
                "priority": member.priority,
                "description": member.description,
            }

        return [Document(page_content=team_info, metadata=team_metadata)]


class ResearchArticle(BaseModel):
    title: str
    abstract: str

    def to_document(self) -> Document:
        return Document(
            page_content=(
                f"Scientific Research on Salinity and Water Quality:\n\n"
                f"Research Title: {self.title}\n\n"
                f"Key Findings and Information:\n{self.abstract}\n\n"
                f"This research paper discusses: {self._extract_key_topics()}\n\n"
                f"Relevant for: {self._extract_relevance()}"
            ),
            metadata={
                "title": self.title,
                "abstract": self.abstract,
                "type": "research_article",
                "used_for": "Scientific research on water quality and salinity",
                "topics": self._extract_key_topics(),
                "keywords": self._extract_keywords(),
                "document_type": "scientific_research",
                "relevance": self._extract_relevance(),
            },
        )

    def _extract_key_topics(self) -> List[str]:
        # Simple keyword-based topic extraction
        topics = []
        text = f"{self.title} {self.abstract}".lower()

        topic_keywords = {
            "salinity": ["salinity", "salt", "salinization", "saltwater"],
            "climate change": ["climate change", "sea level rise", "global warming"],
            "water quality": ["water quality", "contamination", "pollution"],
            "HABs": ["algal bloom", "hab", "harmful algal"],
            "drinking water": ["drinking water", "potable water", "water supply"],
            "chesapeake bay": ["chesapeake", "bay", "estuary"],
            "research methods": ["model", "simulation", "analysis", "study"],
        }

        for topic, keywords in topic_keywords.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)

        return topics

    def _extract_keywords(self) -> List[str]:
        # Extract important keywords for search
        text = f"{self.title} {self.abstract}".lower()
        keywords = []

        important_terms = [
            "salinity",
            "salt",
            "water",
            "climate",
            "research",
            "study",
            "analysis",
            "model",
            "chesapeake",
            "bay",
            "quality",
            "contamination",
            "pollution",
            "algal",
            "bloom",
            "hab",
            "drinking",
            "supply",
            "coastal",
        ]

        for term in important_terms:
            if term in text:
                keywords.append(term)

        return keywords

    def _extract_relevance(self) -> str:
        # Determine who might find this research relevant
        text = f"{self.title} {self.abstract}".lower()
        relevance = []

        if any(term in text for term in ["drinking", "potable", "supply"]):
            relevance.append("water suppliers")
        if any(term in text for term in ["coastal", "shore", "beach"]):
            relevance.append("coastal communities")
        if any(term in text for term in ["model", "simulation", "prediction"]):
            relevance.append("researchers and scientists")
        if any(term in text for term in ["policy", "regulation", "management"]):
            relevance.append("policy makers")
        if any(term in text for term in ["farm", "agriculture", "crop"]):
            relevance.append("agricultural users")

        return ", ".join(relevance) if relevance else "general scientific audience"


class ResearchArticles(BaseModel):
    articles: List[ResearchArticle]

    @classmethod
    def from_csv(cls, file_path: str) -> "ResearchArticles":
        df = pd.read_csv(file_path)

        column_mapping = {"Title": "title", "Abstract": "abstract"}
        df = df.rename(columns=column_mapping)

        return cls(
            articles=[ResearchArticle(**row.to_dict()) for _, row in df.iterrows()]
        )

    def to_documents(self) -> List[Document]:
        return [article.to_document() for article in self.articles]


class VectorDBManager:
    def __init__(self, api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.embedding_size = len(self.embeddings.embed_query("dummy embedding"))

    def create_index(self, index_type: str = "HNSW") -> faiss.Index:
        if index_type == "FlatL2":
            return faiss.IndexFlatL2(self.embedding_size)
        elif index_type == "HNSW":
            return faiss.IndexHNSWFlat(self.embedding_size, 32)
        raise ValueError(f"Invalid index type: {index_type}")

    def create_db(self, index: faiss.Index) -> FAISS:
        return FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )


def main() -> FAISS:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize vector DB manager
    vdb_manager = VectorDBManager(api_key)
    index = vdb_manager.create_index("HNSW")
    db = vdb_manager.create_db(index)

    # Set up directories
    this_dir = os.path.dirname(os.path.abspath(__file__))
    unloaded_dir = os.path.join(this_dir, "unloaded")

    # Load and process interview transcripts
    transcript_files = [
        f for f in os.listdir(unloaded_dir) if f.startswith("TRANSCRIPT_")
    ]
    for file in transcript_files:
        transcript_data = TranscriptData.from_json_file(
            os.path.join(unloaded_dir, file)
        )
        print(f"\n\nTRANSCRIPT DATA:\n\n{transcript_data}\n\n")
        db.add_documents(documents=transcript_data.to_documents())

    # Load and process team list
    team_list_data = TeamListData.from_csv(os.path.join(unloaded_dir, "Team_List.csv"))
    print(f"\n\nTEAM LIST DATA:\n\n{team_list_data}\n\n")
    db.add_documents(documents=team_list_data.to_documents())

    # Load and process research articles
    research_articles = ResearchArticles.from_csv(
        os.path.join(unloaded_dir, "Research-Articles-Learning.csv")
    )
    print(f"\n\nRESEARCH ARTICLES:\n\n{research_articles}\n\n")
    db.add_documents(documents=research_articles.to_documents())

    # Save the database
    db.save_local(os.path.join(this_dir, "TeamListVDB-HNSW"))
    return db


if __name__ == "__main__":
    main()
    print("Vector database created and saved successfully.")
