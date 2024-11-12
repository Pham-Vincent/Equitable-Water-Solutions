"""
Chatbot for Salt Cast

Developers:
- Spencer Presley | github.com/spencerpresley
- Dustin O'Brien | github.com/omniladder
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import logging

from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from .config import ChatbotConfig
from .vectordb_manager import VectorDBManager
from .memory_manager import MemoryManager


class Chatbot:
    """
    Attributes:
        api_key (str): OpenAI API key
        project_name (str): Project identifier (default: "Saltcast")
        database_name (str): Vector database name (default: "index")
        temperature (float): Model creativity (0.0-1.0)
        model_type (str): OpenAI model name
        system_message (str): Instructions for the LLM
        debug (bool): Enable detailed logging
        log_level (Optional[int]): Logging level (see: https://docs.python.org/3/library/logging.html#logging-levels)
            - None: Defaults to DEBUG if debug=True, ERROR if debug=False
            - Can use logging.DEBUG/INFO/WARNING/ERROR/CRITICAL
            - Or integer values: 10/20/30/40/50

    Methods:
        Public:
        __init__(api_key, project_name, database_name, temperature, model_type, system_message, debug, log_level):
            Initializes chatbot components

        process_prompt(prompt: str, session_id: str) -> Generator:
            Processes user input, retrieves relevant docs, streams LLM response, calls _post_response_processing()

        Private:
        _create_chain(llm: ChatOpenAI) -> Runnable:
            Internal method that creates the LLM chain

        _post_response_processing(prompt: str, llm_response: str, session_id: str):
            Updates conversation memory after response completion and loads updated conversation history into memory
    """

    def __init__(
        self,
        api_key: str,
        vector_db_dir: Path = ChatbotConfig.DEFAULT_VECTOR_DB_DIR,
        database_name: str = ChatbotConfig.DEFAULT_DATABASE_NAME,
        temperature: float = ChatbotConfig.DEFAULT_TEMPERATURE,
        model_type: str = ChatbotConfig.DEFAULT_MODEL_TYPE,
        system_message: str = ChatbotConfig.SYSTEM_MESSAGE,
        debug: bool = False,
        log_level: Optional[int] = None,
        **chatbot_kwargs,
    ):
        self.logger = self._setup_logging(debug, log_level)

        self.debug = debug
        self.log_level = log_level

        # Clear any existing handlers
        logging.getLogger().handlers = []

        # Store basic config
        self.vector_db_dir = vector_db_dir
        self.database_name = database_name
        self.api_key = api_key
        self.system_message = system_message

        # Initialize components
        set_llm_cache(InMemoryCache())
        self.llm = self._initialize_llm(
            self.api_key, temperature, model_type, **chatbot_kwargs
        )
        self.embeddings = self._initialize_embeddings(self.api_key)
        self.vectordb_manager = self._initialize_vectordb_manager(
            self.vector_db_dir,
            self.database_name,
            self.embeddings,
        )
        self.memory_manager = self._initialize_memory_manager(self.llm)
        self.conversation_summary = {}

        # Create the AI chain
        self.chain = self._create_chain(self.llm)

    def process_prompt(self, prompt: str, session_id: str):
        """
        Processes user input and streams the response.

        1. Retrieves relevant documents from vector database
        2. Generates response using LLM chain
        3. Streams response chunks to client
        4. Updates conversation memory after completion

        Args:
            prompt (str): User input text
            session_id (str): Session identifier

        Yields:
            str: Response chunks for streaming
            "end-of-stream": Signals response completion
            "event: stream-error\ndata: {error}": On error
        """
        self.logger.info(
            f"Processing prompt: {prompt[:50]}... for session: {session_id}"
        )

        # Initialize the LLM response
        # The purpose for recording the response in this local variable and not
        # just only yielding out the chunks is to be able to update the ConversationSummaryBufferMemory
        llm_response = ""
        try:
            self.logger.info("Starting chain")

            # Retrieve relevant documents for the prompt from vector database
            relevant_docs = self.vectordb_manager.get_relevant_docs(prompt=prompt)
            self.logger.debug(f"RELEVANT DOCS:\n\n{relevant_docs}\n\n")

            # Create the chain variables
            # The keys match the placeholder variables in the prompts found in chatbot/scripts/config.py
            chain_vars = {
                "prompt": prompt,
                "relevant_docs": relevant_docs,
                "conversation_summary": self.conversation_summary.get("history", ""),
            }
            self.logger.info(f"Chain variables created:\n{chain_vars}")

            # Stream the response from the chain
            # chain.stream() is a generator that yields chunks of the response from the language model
            # as they are generated.
            # This block of code acts as a sort of buffer which yields out those chunks to the frontend.
            # It updates the local llm_response variable with each chunk so that the ConversationSummaryBufferMemory
            # can be updated with the latest response from the language model.
            for chunk in self.chain.stream(chain_vars):
                self.logger.info(f"Chunk received:\n{chunk}")
                if chunk.content:
                    self.logger.info(f"Chunk content:\n{chunk.content}")
                    llm_response += chunk.content
                    self.logger.info(f"LLM response updated:\n{llm_response}")
                    yield chunk.content
            yield "end-of-stream"

            self.logger.info("Finished streaming response")
            self.logger.info("Starting post-response processing")

            # Some processes are backloaded after the response is streamed to the frontend.
            # This is because certain things such as updating the ConversationSummaryBufferMemory
            # do not need to happen real time.
            # This is because we do not need to summarize the prompt coming in, as it isn't part of the message history yet.
            # Since this is the most recent message we can treat is as somewhat special and not have is summarized as part of "old messages"
            # So instead we can backload the generation of the conversation summary after a user message + llm response chain has run.
            # This allows the updating of the ConversationSummaryBufferMemory to happen in the "background"
            # Thus alleviating time between a user message input and the beginning of the streaming of the response.
            self._post_response_processing(
                prompt=prompt,
                llm_response=llm_response,
                session_id=session_id,
            )
        except Exception as e:
            self.logger.debug(f"An error occurred in process_prompt: {str(e)}")
            yield f"event: stream-error\ndata: {str(e)}\n\n"

    def _create_chain(self, llm: ChatOpenAI) -> Runnable:
        """
        Creates the LLM processing pipeline.

        Combines:
        1. RunnablePassthrough for input handling
        2. ChatPromptTemplate for message formatting
        3. LLM for response generation

        Args:
            llm (ChatOpenAI): Language model instance

        Returns:
            Runnable: Configured processing chain
        """

        # ChatPromptTemplate.from_messages() is used to create a prompt template from a list of messages
        # What's special about ChatPromptTemplate is you can pass in string representations of messages
        # "system" = system message
        # "human" = user message
        # "ai" = assistant message
        # See here: https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html
        self.logger.info("Creating chain")
        chain = (
            RunnablePassthrough()
            | ChatPromptTemplate.from_messages(
                [
                    ("system", self.system_message),
                    ("human", "{prompt}"),
                ]
            )
            | self.llm
        )
        self.logger.info("Chain set up")
        return chain

    def _post_response_processing(
        self,
        *,
        prompt: str,
        llm_response: str,
        session_id: str,
    ):
        """
        Updates conversation memory with latest interaction.

        Args:
            prompt (str): Original user input
            llm_response (str): Complete model response
            session_id (str): Session identifier

        Note:
            Runs after response streaming to minimize latency
        """
        self.logger.info(f"Starting post-response processing for session: {session_id}")
        try:
            self.logger.info(f"Prompt: {prompt}")
            self.logger.info("-" * 50)
            self.logger.info(f"LLM Response: {llm_response}")
            self.logger.info("-" * 50)

            # Update memories updates the ConversationSummaryBufferMemory with the latest user prompt and the
            # subsequent LLM response to that prompt.
            self.memory_manager.update_memories(
                prompt=prompt, llm_response=llm_response
            )

            # Reload summary into the conversation_summary instance variable so it can
            # be immediatley available to be injected into the next prompt without having to load again.
            self.conversation_summary = self.memory_manager.load_memory_variables(
                prompt=prompt
            )

            self.logger.info("\nConversation Summary:")
            self.logger.info(self.memory_manager.memory)

            self.logger.info("Finished post-response processing")
        except Exception as e:
            self.logger.debug(f"Error in post_response_processing: {str(e)}")
            import traceback

            traceback.print_exc()

    def _setup_logging(self, debug: bool, log_level: Optional[int]):
        """Configure logging based on debug flag and log level."""
        logging.getLogger().handlers = []
        level = log_level or (logging.DEBUG if debug else logging.ERROR)
        logging.basicConfig(level=level)
        logger = logging.getLogger(__name__)
        return logger

    @staticmethod
    def _initialize_llm(
        api_key: str, temperature: float, model_type: str, **chatbot_kwargs
    ):
        return ChatOpenAI(
            api_key=api_key,
            temperature=temperature,
            model=model_type,
            streaming=True,
            **chatbot_kwargs,
        )

    @staticmethod
    def _initialize_embeddings(api_key: str):
        return OpenAIEmbeddings(api_key=api_key)

    @staticmethod
    def _initialize_vectordb_manager(
        vector_db_dir: Path,
        database_name: str,
        embeddings: OpenAIEmbeddings,
    ):
        return VectorDBManager(vector_db_dir, database_name, embeddings)

    @staticmethod
    def _initialize_memory_manager(llm: ChatOpenAI):
        return MemoryManager(llm)
