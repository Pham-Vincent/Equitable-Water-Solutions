from pydantic import BaseModel
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
from pathlib import Path

# Import utility functions for finding directories
from .dir_utils import get_vector_db_dir, find_env_file, find_project_root


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


class VectorDBCreator:
    def __init__(self, api_key: str, index_type: str = "HNSW"):
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
        self.embedding_size = len(self.embeddings.embed_query("dummy embedding"))
        self._validate_index_type(index_type)
        self.index = self._create_index(index_type)
        self.db = None

    def _create_index(self, index_type: str) -> faiss.Index:
        if index_type == "FlatL2":
            try:
                return faiss.IndexFlatL2(self.embedding_size)
            except Exception as e:
                raise ValueError(f"Error creating FlatL2 index: {e}")
        elif index_type == "HNSW":
            try:
                return faiss.IndexHNSWFlat(self.embedding_size, 32)
            except Exception as e:
                raise ValueError(f"Error creating HNSW index: {e}")

    def _validate_index_type(self, index_type: str) -> None:
        if index_type not in ["FlatL2", "HNSW"]:
            raise AttributeError(f"Invalid index type: {index_type}. Must be 'FlatL2' or 'HNSW'.")

    def create_db(self) -> FAISS:
        try:
            self.db =FAISS(
                embedding_function=self.embeddings,
                index=self.index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )
            return self
        except Exception as e:
            raise ValueError(f"Error creating FAISS database: {e}")
    
    def get_db(self) -> FAISS:
        return self.db
    


def main() -> FAISS:
    # Get the directory of the makeVDB.py script
    this_dir = Path(__file__).resolve()
    
    # Define the name of the VectorDB directory
    vector_db_dir_name = "VectorDB"
    
    # Find the VectorDB directory
    vector_db_dir = get_vector_db_dir(start_dir=this_dir, target_dir=vector_db_dir_name)
    vector_data_dir = vector_db_dir / "vectordb_data"
    vectordb_save_dir = vector_db_dir / "vectordb"
    
    # Find the .env file in the project
    env_file = find_env_file(root_dir=find_project_root(this_dir))
    
    # Load the environment variables from the located .env file
    load_dotenv(env_file)

    # Create the vector database
    db = VectorDBCreator(api_key=os.getenv("OPENAI_API_KEY")).create_db().get_db()
    

    # Load and process interview transcripts
    transcript_files = [
        f for f in os.listdir(vector_data_dir) if f.startswith("TRANSCRIPT_")
    ]
    for file in transcript_files:
        transcript_data = TranscriptData.from_json_file(
            os.path.join(vector_data_dir, file)
        )
        print(f"\n\nTRANSCRIPT DATA:\n\n{transcript_data}\n\n")
        db.add_documents(documents=transcript_data.to_documents())

    # Load and process team list
    team_list_data = TeamListData.from_csv(os.path.join(vector_data_dir, "Team_List.csv"))
    print(f"\n\nTEAM LIST DATA:\n\n{team_list_data}\n\n")
    db.add_documents(documents=team_list_data.to_documents())

    # Load and process research articles
    research_articles = ResearchArticles.from_csv(
        os.path.join(vector_data_dir, "Research-Articles-Learning.csv")
    )
    print(f"\n\nRESEARCH ARTICLES:\n\n{research_articles}\n\n")
    db.add_documents(documents=research_articles.to_documents())

    # Save the database
    db.save_local(vectordb_save_dir)


if __name__ == "__main__":
    main()
    print("Vector database created and saved successfully.")
