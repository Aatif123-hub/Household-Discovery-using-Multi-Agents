import logging
from typing import TypedDict, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from . import prompts
from rag.llm import LLM
from rag.vectorstore import VectorStore
from rag.embeddings import Embeddings
import pandas as pd
import os
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    task: str
    result: Optional[str]

def retrieve_rag_context(query, vectorstore, k=20):
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([result.page_content for result in results])

def process_agent(state: AgentState, prompt_template: str, agent_name: str, llm: LLM, vectorstore) -> dict:
    try:
        logger.info(f"Executing {agent_name}")

        rag_context = retrieve_rag_context(state['task'], vectorstore)

        full_prompt = f"""
        You are an expert entity resolution agent. Answer clearly using the provided context.

        Context:
        {rag_context}

        Task Instructions:
        {prompt_template}

        Provide your answer strictly as a markdown table with clear column headers.
        """

        messages = [
            SystemMessage(content=full_prompt.strip()),
            HumanMessage(content=state["task"])
        ]
        response = llm.invoke(messages)

        response_content = response.content if response and hasattr(response, 'content') else "No response generated"
        return {"result": response_content}

    except Exception as e:
        logger.error(f"Error in {agent_name}: {e}")
        return {"result": f"Error: {e}"}

def direct_agent_node(state: AgentState, llm: LLM, vectorstore) -> dict:
    return process_agent(state, prompts.direct_matcher, "Direct Match Agent", llm, vectorstore)

def indirect_agent_node(state: AgentState, llm: LLM, vectorstore) -> dict:
    return process_agent(state, prompts.indirect_matcher, "Indirect Match Agent", llm, vectorstore)

def household_agent_node(state: AgentState, llm: LLM, vectorstore) -> dict:
    return process_agent(state, prompts.household_matcher, "Household Match Agent", llm, vectorstore)

def household_moves_agent_node(state: AgentState, llm: LLM, vectorstore) -> dict:
    return process_agent(state, prompts.household_moves, "Household Moves Agent", llm, vectorstore)

def build_graph(llm: LLM, embedding_model: str, vector_store: str, text_chunks: list) -> StateGraph:
    embeddings = Embeddings.get_embeddings(embedding_model)
    vectorstore = VectorStore.vectorization(vector_store, text_chunks, embeddings)

    memory = MemorySaver()
    builder = StateGraph(state_schema=AgentState)

    builder.add_node("direct_agent", lambda state: direct_agent_node(state, llm, vectorstore))
    builder.add_node("indirect_agent", lambda state: indirect_agent_node(state, llm, vectorstore))
    builder.add_node("household_agent", lambda state: household_agent_node(state, llm, vectorstore))
    builder.add_node("household_moves_agent", lambda state: household_moves_agent_node(state, llm, vectorstore))

    builder.set_entry_point("direct_agent")
    builder.add_edge("direct_agent", "indirect_agent")
    builder.add_edge("indirect_agent", "household_agent")
    builder.add_edge("household_agent", "household_moves_agent")
    builder.add_edge("household_moves_agent", END)

    return builder.compile(checkpointer=memory)
