from langchain.memory import ConversationSummaryBufferMemory, ConversationEntityMemory
from langchain_openai import ChatOpenAI
from .config import ChatbotConfig
from .utils.memory_utils import update_memory, update_entity_memory
from typing import Optional

class MemoryManager:
    def __init__(
        self,
        llm: ChatOpenAI
    ):
        self.llm = llm
        self.memory: ConversationSummaryBufferMemory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=ChatbotConfig.MEMORY_TOKEN_LIMIT,
            return_messages=True,
        )
        self.entityMemory: ConversationEntityMemory = ConversationEntityMemory(
            llm=self.llm,
            k=ChatbotConfig.ENTITY_MEMORY_K,
        )
        
    async def update_memories(self, prompt: str, llm_response: str):
        await update_memory(self.memory, prompt, llm_response)
        await update_entity_memory(self.entityMemory, prompt, llm_response)
        
    def load_memory_variables(self, *, prompt: Optional[str] = None):
        conversation_summary = self.memory.load_memory_variables({})
        conversation_entities = self.entityMemory.load_memory_variables({"input": prompt} if prompt else {})
        conversation_entities.pop("history", None)
        return conversation_summary, conversation_entities