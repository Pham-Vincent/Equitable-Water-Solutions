import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from .config import ChatbotConfig
from .utils.document_processing import get_relevant_docs
from typing import List

class VectorDBManager:
    def __init__(
        self,
        project_name: str,
        database_name: str,
        embeddings: OpenAIEmbeddings
    ):
        self.project_name = project_name
        self.database_name = database_name
        self.embeddings = embeddings
        self.database = self.load_database()
        
    def load_database(self) -> FAISS:
        """
        Load the FAISS database for the specified project and database name.

        Returns:
            FAISS: The loaded FAISS database.

        Raises:
            RuntimeError: If the database fails to load.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(
            script_dir, "..", "projects", self.project_name, "docs", "AllDocumentsVDB"
        )

        try:
            return FAISS.load_local(
                database_path,
                self.embeddings,
                self.database_name,
                allow_dangerous_deserialization=True,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load database: {e}")
        
    def get_relevant_docs(self, *, prompt: str) -> List[str]:
        return get_relevant_docs(database=self.database, prompt=prompt)