from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS


def summarize_docs(llm: ChatOpenAI, docs: List[str]) -> str:
    """
    Summarize the given documents.
    """
    summarize_prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize the following text in a concise manner:\n\n{text}",
    )
    summarize_chain = summarize_prompt | llm | RunnablePassthrough()
    summary = summarize_chain.invoke({"text": " ".join(docs)})
    return summary


def extract_entities(*, llm: ChatOpenAI, docs: List[str]) -> str:
    """
    Extract entities from the given documents.
    """
    entity_prompt = PromptTemplate(
        input_variables=["text"],
        template="Extract key entities (e.g., people, places, concepts) from the following text:\n\n{text}",
    )
    entity_chain = entity_prompt | llm | RunnablePassthrough()
    entities = entity_chain.invoke({"text": " ".join(docs)})
    return entities


def get_relevant_docs(
    *, database: FAISS, prompt: str, max_docs: Optional[int] = 3, score_threshold: Optional[float] = 0.5
) -> List[str]:
    """
    Retrieve relevant documents from the database based on the given prompt.

    Args:
        database (FAISS): The FAISS database to search.
        prompt (str): The prompt to search for relevant documents.
        max_docs (int): Maximum number of documents to return. Defaults to 3.
        score_threshold (float): Maximum L2 distance to consider a document relevant. Defaults to 1.0.

    Returns:
        List[str]: A list of relevant document contents.
    """
    try:
        # Fetch documents with scores
        docs_and_scores = database.similarity_search_with_score(prompt, k=max_docs)

        # Filter and limit the documents
        relevant_docs = [
            doc.page_content
            for doc, score in docs_and_scores
            if score <= score_threshold
        ][:max_docs]

        return relevant_docs
    except Exception as e:
        print(f"Warning: Failed to retrieve relevant documents: {e}")
        return []
