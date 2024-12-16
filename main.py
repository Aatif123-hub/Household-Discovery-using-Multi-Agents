from dotenv import load_dotenv
load_dotenv()

from textwrap import dedent
from crewai import Agent, Crew

from tasks.directmatcher_task import DirectMatcherTasks
from tasks.indirectmatcher_task import IndirectMatcherTasks
from tasks.householdmatcher_task import HouseholdMatcherTasks
from tasks.householdmoves_task import HouseholdMovesTasks

from agents.direct_matcher import DirectMatchAgent
from agents.indirect_matcher import IndirectMatchAgent
from agents.household_matcher import HouseholdMatchAgent
from agents.householdmoves_matcher import HouseholdMovesAgent

import os
import streamlit as st
from utils.parser import Parsers
from utils.chunking import Chunking
from rag.embeddings import Embeddings
from rag.vectorstore import VectorStore
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.retrievers.multi_query import MultiQueryRetriever
from rag.llm import LLM

print("## Welcome to the Household Discovery Pipeline")
print('-------------------------------------------')

# Collect input from the user
selected_files = input("Enter the paths of the selected files (comma-separated):\n").split(',')
embedding_model = input("Enter the embedding model to use:\n")
vector_store = input("Enter the vector storage type to use:\n")
llm_model = input("Enter the LLM model to use:\n")

# Initialize Agents
direct_match_agent = DirectMatchAgent()
indirect_match_agent = IndirectMatchAgent()
household_match_agent = HouseholdMatchAgent()
household_moves_agent = HouseholdMovesAgent()

# Initialize Tasks
direct_match_task = DirectMatcherTasks.direct_matcher_task(direct_match_agent, selected_files, embedding_model)
indirect_match_task = IndirectMatcherTasks.indirect_matcher_task(indirect_match_agent, selected_files, embedding_model)
household_match_task = HouseholdMatcherTasks.household_matcher_task(household_match_agent, selected_files, embedding_model)
household_movement_task = HouseholdMovesTasks.household_moves_task(household_moves_agent, selected_files, embedding_model)

# Process Files
combined_text = ""
for selected_file in selected_files:
    if selected_file.endswith('.csv'):
        combined_text += Parsers.csv_parser([selected_file]).to_string()
    elif selected_file.endswith('.xlsx'):
        combined_text += Parsers.xlsx_parser([selected_file]).to_string()
    else:
        raise ValueError("Unsupported file type. Please select a CSV or XLSX file.")

if not combined_text.strip():
    raise ValueError("No text extracted from the selected files.")

# Generate Chunks and Embeddings
text_chunks = Chunking.get_chunks(combined_text)
embeddings = Embeddings.get_embeddings(embedding_model)
vectorstore = VectorStore.vectorization(vector_store, text_chunks, embeddings)

# Setup LLM and Retrieval Chain
llm = LLM.get_llm(llm_model)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

multi_query_retriever = MultiQueryRetriever.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
)

conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=multi_query_retriever,
    memory=memory,
    verbose=True
)

response = conversation_chain({"question": "Provide a summary of the data analysis."})
summary = response['answer']

# Create Crew for Matching Pipeline
matching_crew = Crew(
    agents=[
        direct_match_agent,
        indirect_match_agent,
        household_match_agent,
        household_moves_agent
    ],
    tasks=[
        direct_match_task,
        indirect_match_task,
        household_match_task,
        household_movement_task
    ],
    verbose=True
)

# Execute Matching Pipeline
pipeline_results = matching_crew.kickoff()

# Save Summary and Results
output_folder = "/Users/aatif/household_discovery/output"
os.makedirs(output_folder, exist_ok=True)
output_file_path = os.path.join(output_folder, "output_summary.md")

with open(output_file_path, "w") as output_file:
    output_file.write(f"# Summary\n\n{summary}\n")
    output_file.write("\n#\n")
    output_file.write(f"Pipeline Results:\n{pipeline_results}\n")

# Display Final Results
print("\n\n########################")
print("## Pipeline Results")
print("########################\n")
print("Results:")
print(pipeline_results)
print("\nSummary:\n", summary)
