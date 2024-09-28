from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


async def update_memory(memory, prompt, llm_response):
    print("Updating memory...")
    memory.save_context({"input": prompt}, {"output": llm_response})
    print("Memory updated.")


async def update_entity_memory(entity_memory, prompt, llm_response):
    print("Updating entity memory...")
    entity_memory.save_context({"input": prompt}, {"output": llm_response})
    print("Entity memory updated.")
