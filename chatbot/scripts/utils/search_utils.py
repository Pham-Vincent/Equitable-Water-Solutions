from typing import List, Tuple
import re
from functools import lru_cache
import json
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field


class WebSearchDecision(BaseModel):
    web_search_needed: bool = Field(
        description="Whether a web search is needed to answer the query"
    )
    reason: str = Field(description="Reason for the decision")


def web_search(search_engine, query: str, num_results: int = 3) -> List[str]:
    print(f"Performing web search for query: {query}")
    try:
        results = search_engine.run(query)
        print("Raw search results:")
        print(results)

        # Split the results into individual entries
        entries = results.split("\n")

        formatted_results = []
        current_entry = ""
        for line in entries:
            if line.strip():  # If the line is not empty
                current_entry += line + "\n"
            elif current_entry:  # If we have a complete entry
                formatted_results.append(current_entry.strip())
                current_entry = ""

        if current_entry:  # Add the last entry if it exists
            formatted_results.append(current_entry.strip())

        # Limit to num_results
        formatted_results = formatted_results[:num_results]

        print("Formatted search results:")
        for result in formatted_results:
            print(result)
            print("---")

        return formatted_results
    except Exception as e:
        print(f"Error performing search for query '{query}': {str(e)}")
        import traceback

        traceback.print_exc()
        return []


def format_citations(sources: List[str]) -> Tuple[str, str]:
    print("Input sources for citations:")
    for source in sources:
        print(source)
        print("---")

    citations = []
    citation_guide = "Web Sources:\n"

    for i, source in enumerate(sources, start=1):
        # Extract the first line as the title
        title = source.split("\n")[0] if "\n" in source else source
        citations.append(f"[{i}]")
        citation_guide += f"[{i}] {title}\n"

    print("Formatted citations:", " ".join(citations))
    print("Citation guide:")
    print(citation_guide)

    return " ".join(citations), citation_guide


@lru_cache(maxsize=100)
def simple_should_web_search(prompt: str) -> bool:
    keywords = [
        "latest",
        "current",
        "recent",
        "news",
        "update",
        "today",
        "web search",
        "look it up",
        "do research",
        "find out",
        "find information",
        "find data",
        "find statistics",
        "find facts",
        "find figures",
        "find numbers",
        "find details",
    ]
    greetings = [r"\bhi\b", r"\bhello\b", r"\bhey\b", r"how are you", r"what\'s up"]

    if any(keyword in prompt.lower() for keyword in keywords):
        return True
    if any(re.search(pattern, prompt.lower()) for pattern in greetings):
        return False
    return False


async def should_web_search(llm, prompt: str, web_search_cache: dict) -> bool:
    if prompt in web_search_cache:
        return web_search_cache[prompt]

    simple_result = simple_should_web_search(prompt)
    if simple_result is not None:
        web_search_cache[prompt] = simple_result
        return simple_result

    system_message = SystemMessage(
        content="You are an AI assistant tasked with determining whether a web search is necessary to answer a user's query. Consider whether the information required is likely to be current events, rapidly changing data, or information that might not be in a typical knowledge base."
    )
    human_message = HumanMessage(
        content=f"Based on the following user query, determine if a web search is necessary to provide an accurate and up-to-date answer: '{prompt}'"
    )

    prompt_template = PromptTemplate(
        template="System: {system}\nHuman: {human}\nAI: Analyze the query and determine if a web search is necessary. Respond in JSON format with 'web_search_needed' (boolean) and 'reason' (string).",
        input_variables=["system", "human"],
    )

    chain = (
        {"system": RunnablePassthrough(), "human": RunnablePassthrough()}
        | prompt_template
        | llm
    )

    response = await chain.ainvoke(
        {"system": system_message.content, "human": human_message.content}
    )

    try:
        decision = json.loads(response.content)
        result = decision.get("web_search_needed", False)
    except json.JSONDecodeError:
        print(f"Failed to parse LLM response as JSON: {response.content}")
        result = False

    web_search_cache[prompt] = result
    return result


def generate_search_query(search_query_chain, original_query: str) -> str:
    return search_query_chain.run(original_query=original_query)
