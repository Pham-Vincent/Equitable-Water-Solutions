from .chatbot import Chatbot
from pydantic import BaseModel as PydanticBaseModel


def get_chatbot():
    return Chatbot()


class InitializeRequest(PydanticBaseModel):
    project_name: str = "Salinity"
    database_name: str = "main"
    session_id: str = ""
