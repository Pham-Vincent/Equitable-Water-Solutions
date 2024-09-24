"""
Developers:
- Spencer Presley | github.com/spencerpresley
- Dustin O'Brien | github.com/omniladder

Chatbot Module for Salt Cast Project

This module implements a sophisticated chatbot system for the Salt Cast research project,
focusing on salinity levels in the Chesapeake Bay. Key features include:

1. Integration with OpenAI's language models and FAISS vector database for contextual understanding and document retrieval.
2. Conversation memory using ConversationSummaryBufferMemory and ConversationEntityMemory to maintain context across sessions.
3. Web search capabilities using DuckDuckGo for up-to-date information, enhancing response accuracy.
4. Asynchronous processing of prompts with streaming responses to handle real-time user interactions efficiently.
5. Context-aware responses prioritizing project-specific knowledge to provide tailored information.
6. Entity extraction and management from conversations and relevant documents to enrich the chatbot's understanding.
7. Citation handling for web search results to maintain transparency and reliability.
8. Flexible initialization with customizable parameters (project name, database, model, etc.) to adapt to different project needs.
9. Error handling and extensive logging (printing) for debugging to ensure robustness and ease of maintenance.

The Chatbot class encapsulates all functionalities, providing methods for processing prompts,
managing conversation context, and handling post-response operations.

Chatbot uses a variety of helper modules to perform its tasks. These modules are located in the `src/scripts` and `scr/scripts/utils` directories.

The Chatbot's configuartion can be found in the `src/scripts/config.py` file.
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Dict, List, Optional, AsyncGenerator

from langchain.cache import InMemoryCache
from langchain.chains import LLMChain
from langchain.globals import set_llm_cache
from langchain.prompts import PromptTemplate

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.output_parsers import JsonOutputParser

from langchain_openai import ChatOpenAI, OpenAIEmbeddings 

from .utils import *
from .utils.document_processing import extract_entities
from .config import ChatbotConfig
from .vectordb_manager import VectorDBManager
from .memory_manager import MemoryManager

class Chatbot:
    """
    Encapsulates the chatbot functionality for the Salt Cast Project.
    This class integrates various components such as language models, vector databases, and web search APIs to provide a responsive and intelligent chatbot.
    """

    def __init__(
        self,
        project_name: str = ChatbotConfig.DEFAULT_PROJECT_NAME,
        database_name: str = ChatbotConfig.DEFAULT_DATABASE_NAME,
        temperature: float = ChatbotConfig.DEFAULT_TEMPERATURE,
        model_type: str = ChatbotConfig.DEFAULT_MODEL_TYPE,
        system_messages: str = ChatbotConfig.SYSTEM_MESSAGES,
    ):
        """
        Initializes the Chatbot with necessary components.

        Args:
            project_name (str): The name of the project.
            database_name (str): The name of the database.
            temperature (float): The temperature setting for the language model. Defaults to 0.65. Range is 0.0 (most deterministic) to 1.0 (most random).
            model_type (str): Model to be used, accepts any OpenAI models. Defaults to gpt-4o-mini. gpt-4o provides better results and is faster but also more expensive.
            system_messages (Optional[dict]): Predefined system messages loaded from a static file. Defaults to None.

        Initializes components like language models, vector databases, and web search APIs. Sets up in-memory caching to optimize API call efficiency.
        """
        self.project_name = project_name
        self.database_name = database_name
        self.api_key = get_openai_api_key()

        # Set up in-memory cache to prevent api calls for identical prompts
        set_llm_cache(InMemoryCache())

        self.llm = ChatOpenAI(
            api_key=self.api_key,
            temperature=temperature,
            model=model_type,
            streaming=True,
        )
        self.embeddings: OpenAIEmbeddings = OpenAIEmbeddings(api_key=self.api_key)
        self.vectordb_manager = VectorDBManager(self.project_name, self.database_name, self.embeddings)
        self.memory_manager = MemoryManager(self.llm)
        
        self.global_chat_history: List[str] = []

        # For frontend display
        self.chat_history: List[str] = []
        self.system_messages: dict = system_messages if system_messages else ChatbotConfig.SYSTEM_MESSAGES
                
    def load_system_messages(self) -> dict:
        """
        Loads the system message(s) from a static folder.

        Returns:
            dict: A dictionary containing system message(s).
        
        This method reads the system message(s) from a JSON file located in a predefined path.
        """
        system_messages: Dict[str, str] = {}

        script_dir: str = os.path.dirname(os.path.abspath(__file__))
        system_messages_path: str = os.path.join(
            script_dir, ChatbotConfig.SYSTEM_MESSAGES_PATH
        )
        with open(system_messages_path, "r") as f:
            system_messages: Dict[str, str] = json.load(f)

        return system_messages
    
    def process_prompt(
        self, prompt: str, session_id: str
    ):
        """
        Processes the given prompt, performs necessary searches, and generates a response.

        Args:
            prompt (str): The user's query.
            session_id (str): The session identifier for tracking conversation context and saving messages to sql database.
            request (Request, optional): The HTTP request context, used for handling disconnections in streaming responses.

        Returns:
            str: The final response generated by the chatbot, or an error message.

        This method orchestrates the entire response generation process, including web and ArXiv searches, document retrieval, and conversation context management. It handles streaming responses for UI display.
        """
        print("Entering process_prompt method")
        llm_response: str = ""
        try:
            print(f"Processing Prompt: {prompt[:50]}... for session: {session_id}")

            # Retrive and process relevant documents from the FAISS database
            try:
                relevant_docs: List[str] = self.vectordb_manager.get_relevant_docs(prompt=prompt)
                print("Retrieved relevant docs")
                print(relevant_docs)

                if relevant_docs:
                    # Extract entities from relelvant documents to provide additional context
                    relevant_docs_entities: Dict[str, List[str]] = extract_entities(
                        llm=self.llm, docs=relevant_docs
                    )
                    print("Extracted entities from docs")
                    print(relevant_docs_entities)
                else:
                    relevant_docs_summary: str = ""
                    relevant_docs_entities: Dict[str, List[str]] = ""
                    print("No relevant docs found")
            except Exception as e:
                print(f"Error processing relevant docs: {str(e)}")
                relevant_docs_summary: str = ""
                relevant_docs_entities: Dict[str, List[str]] = ""

            # Load conversation memory to maintain context across interactions
            try:
                # Retrieve conversation summary from buffer memory
                conversation_summary, conversation_entities = self.memory_manager.load_memory_variables(prompt=prompt)
                print("Conversation summary loaded")
                print(conversation_summary)
                print("Conversation entities loaded")
                print(conversation_entities)
            except Exception as e:
                print(f"Error loading memory variables: {str(e)}")
                raise

             # Prepare the context for the LLM
            context_params = {
                "relevant_docs": relevant_docs,
                "relevant_docs_entities": relevant_docs_entities,
                "conversation_summary": conversation_summary.get("history", "No previous conversation."),
                "conversation_entities": ", ".join(conversation_entities.get("entities", {}).keys()),
            }
            
            # Prepare the context for the LLM, including web results if necesarry
            context_template = ChatbotConfig.CONTEXT_TEMPLATE_WITHOUT_SEARCH
            context = context_template.format(**context_params)

            print("Context prepared for LLM")

            # Prepare messages for the LLM, including system message and user query with context
            messages: List[BaseMessage] = [
                SystemMessage(content=ChatbotConfig.SYSTEM_MESSAGES),
                HumanMessage(content=f"Context: {context}\n\nUser Query: {prompt}"),
            ]

            print("Prepared messages for LLM")

            # This asynchronous generator function streams the response from the LLM in chunks.
            # It formats each chunk for HTML display and checks for disconnection requests.
            try:
                for chunk in self.llm.stream(messages):
                    if chunk.content:
                        llm_response += chunk.content
                        yield chunk.content
                yield "end-of-stream"
                
                self.post_response_processing(
                    prompt=prompt,
                    llm_response=llm_response,
                    session_id=session_id,
                )
            
            except Exception as e:
                print(f"An error occurred in process_prompt: {str(e)}")
                yield f"event: stream-error\ndata: {str(e)}\n\n"
                
        except Exception as e:
            print(f"An error occurred in process_prompt: {str(e)}")
            import traceback
            traceback.print_exc()
            yield f"event: stream-error\ndata: An error occurred in while processing the prompt: {str(e)}"

        return llm_response

    def post_response_processing(
        self,
        *,
        prompt: str,
        llm_response: str,
        session_id: str,
        markdown_response: Optional[str] = None,
        conversation_summary: Optional[dict] = None,
        conversation_entities: Optional[dict] = None,
    ):
        """
        Handles post-response tasks such as updating conversation memories and saving messages to the database.

        Args:
            prompt (str): The original user prompt.
            llm_response (str): The response generated by the language model.
            session_id (str): The session identifier for tracking conversation context.
            conversation_summary (Optional[dict]): The current state of the conversation summary.
            conversation_entities (Optional[dict]): The current state of the conversation entities.

        This method ensures that the chatbot's state is updated with the latest interaction details. It saves the conversation history to the sql database and updates the langchain memories (summary and entitiy).
        """
        try:
            print(f"Starting post-response processing for session: {session_id}")
            print("-" * 50)
            print(f"Prompt: {prompt}")
            print("-" * 50)
            print(f"LLM Response: {llm_response}")
            print("-" * 50)
            print(f"Markdown Response: {markdown_response}")
            print("-" * 50)
            self.memory_manager.update_memories(prompt=prompt, llm_response=llm_response)

            # Reload summary and entities after updating
            updated_summary, updated_entities = self.memory_manager.load_memory_variables(prompt=prompt)
            print("Updated entities:", self.memory_manager.entityMemory.entity_store)

            # Print updated ConversationSummaryBufferMemory contents
            print("\nConversation Summary:")
            print(pretty_print_json(obj=updated_summary))

            # Print updated ConversationEntityMemory contents
            print("\nConversation Entities:")
            print(pretty_print_json(obj=updated_entities))

            self.global_chat_history.append(AIMessage(content=llm_response))

            print("Finished post-response processing")
        except Exception as e:
            print(f"Error in post_response_processing: {str(e)}")
            import traceback
            traceback.print_exc()
