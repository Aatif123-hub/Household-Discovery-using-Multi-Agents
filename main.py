
import os
import streamlit as st
from utils.parser import Parsers
from utils.chunking import Chunking
from rag.embeddings import Embeddings
from crewai import Crew
from rag.vectorstore import VectorStore
from rag.llm import LLM
from multiagents.agents import ER_AGENTS
from multiagents.tasks import ER_TASKS

def rag_pipeline(selected_files, embedding_model, vector_store, llm_model):
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

    text_chunks = Chunking.get_chunks(combined_text)
    embeddings = Embeddings.get_embeddings(embedding_model)
    vectorstore = VectorStore.vectorization(vector_store, text_chunks, embeddings)

    llm = LLM.get_llm(llm_model)

    # Initialize ER_AGENTS with the selected LLM model
    er_agents = ER_AGENTS(llm_model)

    direct_match = er_agents.direct_match()
    indirect_match = er_agents.indirect_match()
    household_match = er_agents.household_match()
    household_moves = er_agents.household_moves()

    direct_matcher = ER_TASKS.direct_matcher_task(direct_match)
    indirect_matcher = ER_TASKS.indirect_matcher_task(indirect_match)
    household_matcher = ER_TASKS.household_matcher_task(household_match)
    household_movement = ER_TASKS.household_moves_task(household_moves)

    crew = Crew(
        agents=[direct_match, indirect_match, household_match, household_moves],
        tasks=[direct_matcher, indirect_matcher, household_matcher, household_movement],
        verbose=True
    )
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    st.title("Entity Resolution with LLM")

    input_folder = "/Users/aatif/Household-Discovery-using-Multi-Agents/input"
    output_folder = "/Users/aatif/Household-Discovery-using-Multi-Agents/output"
    os.makedirs(output_folder, exist_ok=True)
    available_files = [f for f in os.listdir(input_folder) if f.endswith(( '.csv', '.xlsx'))]

    uploaded_files = st.file_uploader("Upload a CSV or XLSX file:", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            with open(os.path.join(input_folder, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            available_files.append(uploaded_file.name)

    if not available_files:
        st.write("No CSV or XLSX files found in the folder.")
    else:
        selected_files_paths = [os.path.join(input_folder, file) for file in available_files]
        
        available_embeddings = Embeddings.get_available_embeddings()
        embedding_model = st.selectbox("Select an embedding model:", available_embeddings)

        available_vectorstores = VectorStore.get_available_vectorstores()
        vector_store = st.selectbox("Select a vector storage type:", available_vectorstores)

        available_llms = LLM.get_available_llm()
        llm_model = st.selectbox("Select an LLM model:", available_llms)

        if st.button("Run Pipeline"):
            try:
                combined_response = rag_pipeline(selected_files_paths, embedding_model, vector_store, llm_model)
                
                output_file_path = os.path.join(output_folder, "output_summary.md")
                with open(output_file_path, "w") as output_file:
                    output_file.write(f"# Summary\n\n{combined_response}\n")
                    output_file.write("\n#\n")

                st.success(f"Summary saved to {output_file_path}")
                st.write("## Summary\n", combined_response)
            except Exception as e:
                st.error(f"Error: {e}")
