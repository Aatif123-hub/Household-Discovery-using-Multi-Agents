import streamlit as st
import os
import logging
from langgraph.graph import END
from utils.parser import Parsers
from utils.chunking import Chunking
from rag.embeddings import Embeddings
from rag.vectorstore import VectorStore
from rag.llm import LLM
from multiagents.graph import build_graph
from langchain_core.messages import SystemMessage, HumanMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    graph = build_graph(llm)

    initial_state = {"task": "Entity Resolution", "result": ""}
    thread = {"configurable": {"thread_id": "1"}}

    for state in graph.stream(initial_state, thread):
        agent_name = list(state.keys())[0]
        agent_result = state[agent_name]
        
        if isinstance(agent_result, dict) and agent_result.get('result'):
            st.subheader(f"{agent_name.replace('_', ' ').title()} Result:")
            st.write(agent_result['result'])
        else:
            st.error(f"Unexpected format in agent response: {agent_result}")

    return state.get('result', 'No result produced.')

def main():
    st.title("Entity Resolution with LLM")
    st.subheader("Multi-Agent System for Data Processing")
    
    input_folder = "./input"
    output_folder = "./output"
    os.makedirs(output_folder, exist_ok=True)
    available_files = [f for f in os.listdir(input_folder) if f.endswith(('.csv', '.xlsx'))]
    
    uploaded_files = st.file_uploader("Upload a CSV or XLSX file:", type=["csv", "xlsx"], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(input_folder, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            available_files.append(uploaded_file.name)

    if not available_files:
        st.write("No CSV or XLSX files found in the folder.")
        return

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

            st.success(f"Summary saved to {output_file_path}")
            st.write("## Summary\n", combined_response)
        except Exception as e:
            st.error(f"Error: {e}")
 


if __name__ == "__main__":
    main()