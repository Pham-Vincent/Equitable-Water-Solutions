class ChatbotConfig:
    DEFAULT_PROJECT_NAME = "Salinity"
    DEFAULT_DATABASE_NAME = "index"
    DEFAULT_TEMPERATURE = 0.65
    DEFAULT_MODEL_TYPE = "gpt-4o-mini"
    MEMORY_TOKEN_LIMIT = 1000
    ENTITY_MEMORY_K = 5  # or whatever value you prefer
    SEARCH_QUERY_TEMPLATE = "Given the user's query: '{original_query}', generate a search query to find the most relevant and up-to-date information online. The search query should be short and focused."
    SYSTEM_MESSAGES_PATH = "static/system_messages.json"
    DATABASE_PATH = ".."
    CONTEXT_TEMPLATE_WITH_SEARCH = """Your main context comes from relevant documents and the conversation history. Use this information as your primary source:

    Relevant Document Summary: {relevant_docs}
    Relevant Document Entities: {relevant_docs_entities}
    Conversation Summary: {conversation_summary}
    Conversation Entities: {conversation_entities}

    Additionally, a web search has been performed to provide supplementary, up-to-date information. Use this to augment your response if needed:

    {web_search_results}

    Citations: {citations}

    Citation Guide:
    {citation_guide}

    Prioritize information from the relevant documents and conversation history, using the web search results only to provide additional context or current information when necessary.
    """
    CONTEXT_TEMPLATE_WITHOUT_SEARCH = """Your main context comes from relevant documents and the conversation history. Use this information as your primary source:

    Relevant t DocumenSummary: {relevant_docs}
    Relevant Document Entities: {relevant_docs_entities}
    Conversation Summary: {conversation_summary}
    Conversation Entities: {conversation_entities}

    No web search was performed for this query. Please provide an answer based primarily on the information from relevant documents and the conversation history. Use your general knowledge to supplement this information if needed.

    If you need up-to-date information that might not be in your knowledge base or the provided context, please indicate that a web search might be necessary for the most current data.
    """
    SYSTEM_MESSAGES = """You are an AI assistant for the research project 'Salt Cast' (formerly known as 'Equitable Water Solutions'). 
    This project focuses on studying salinity levels in the Chesapeake Bay and includes a model that can project salinity changes over a 50-year period. 
    Your primary knowledge comes from the project's research data and documents. 
    If web search results are provided in the context, use them as supplementary information to offer up-to-date insights when relevant.
    Always prioritize information from the project's documents and research data.
    If asked about current events or data not related to the project, clarify that your expertise is centered on the Salt Cast project and Chesapeake Bay salinity projections."""
