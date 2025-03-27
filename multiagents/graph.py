

import logging
from typing import TypedDict, Optional
import pandas as pd
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from . import prompts
from rag.llm import LLM  # Ensure LLM is correctly imported and instantiated

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    task: str
    result: Optional[str]

def get_llm_instance() -> LLM:
    llm = LLM.get_llm("gpt-4")
    if not isinstance(llm, LLM):
        raise TypeError("Expected an instance of LLM but received a different type.")
    return llm

def process_agent(state: AgentState, prompt_template: str, agent_name: str, llm: LLM) -> dict:
    try:
        logger.info(f"Executing {agent_name}")
        messages = [
            SystemMessage(content=prompt_template),
            HumanMessage(content=state['task'])
        ]
        response = llm.invoke(messages) if messages else None

        response_content = response.content if response and hasattr(response, 'content') else "No response generated"

        result_data = {
            "Agent": [agent_name],
            "Task": [state['task']],
            "Response": [response_content]
        }
        df = pd.DataFrame(result_data)
        return {"result": df.to_string(index=False)}
    except Exception as e:
        logger.error(f"Error in {agent_name}: {e}")
        return {"result": f"Error in {agent_name}: {e}"}

def direct_agent_node(state: AgentState, llm: LLM) -> dict:
    return process_agent(state, prompts.direct_matcher, "Direct Match Agent", llm)

def indirect_agent_node(state: AgentState, llm: LLM) -> dict:
    return process_agent(state, prompts.indirect_matcher, "Indirect Match Agent", llm)

def household_agent_node(state: AgentState, llm: LLM) -> dict:
    return process_agent(state, prompts.household_matcher, "Household Match Agent", llm)

def household_moves_agent_node(state: AgentState, llm: LLM) -> dict:
    return process_agent(state, prompts.household_moves, "Household Moves Agent", llm)

def build_graph(llm: LLM) -> StateGraph:
    memory = MemorySaver()
    builder = StateGraph(state_schema=AgentState)

    builder.add_node("direct_agent", lambda state: direct_agent_node(state=state, llm=llm))
    builder.add_node("indirect_agent", lambda state: indirect_agent_node(state=state, llm=llm))
    builder.add_node("household_agent", lambda state: household_agent_node(state=state, llm=llm))
    builder.add_node("household_moves_agent", lambda state: household_moves_agent_node(state=state, llm=llm))

    builder.set_entry_point("direct_agent")
    builder.add_edge("direct_agent", "indirect_agent")
    builder.add_edge("indirect_agent", "household_agent")
    builder.add_edge("household_agent", "household_moves_agent")
    builder.add_edge("household_moves_agent", END)

    return builder.compile(checkpointer=memory)
