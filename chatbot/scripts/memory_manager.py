from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from .config import ChatbotConfig


class MemoryManager:
    def __init__(self, llm: ChatOpenAI):
        self.llm: ChatOpenAI = llm
        self.memory: ConversationSummaryBufferMemory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=ChatbotConfig.MEMORY_TOKEN_LIMIT,
            return_messages=True,
        )

    def update_memories(self, prompt: str, llm_response: str):
        self.memory.save_context({"input": prompt}, {"output": llm_response})

    def load_memory_variables(self, *, prompt):
        conversation_summary = self.memory.load_memory_variables({"input": prompt})
        return conversation_summary
