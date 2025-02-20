import os
import streamlit as st
from utils.parser import Parsers
from rag.embeddings import Embeddings
from rag.vectorstore import VectorStore
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.retrievers.multi_query import MultiQueryRetriever
from rag.llm import LLM

def rag_pipeline(selected_files, embedding_model, vector_store, llm_model, use_existing_vector):
    vectorstore_path = "/Users/aatif/Household-Discovery-using-Multi-Agents/stored_vectors/store_index"
    embeddings = Embeddings.get_embeddings(embedding_model)

    try:
        if use_existing_vector:
            vectorstore = VectorStore.load_local(vectorstore_path, vector_store, embeddings)
            st.info(f"Loaded existing {vector_store} vectorstore from disk.")
        else:
            vectorstore = None
    except Exception as e:
        st.warning(f"Could not load vectorstore: {e}. Creating a new one...")
        vectorstore = None

    if not vectorstore:
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
        if not combined_text.strip():
            raise ValueError("No text extracted from the selected files.")
        
        text_chunks = combined_text.split("\n")
        vectorstore = VectorStore.vectorization(vector_store, text_chunks, embeddings)

        if vectorstore:
            print("New vectorstore created successfully.")
        else:
            raise ValueError("Failed to create the vectorstore.")

    # Continue with LLM and retrieval chain setup
    llm = LLM.get_llm(llm_model)
    with open('/Users/aatif/Household-Discovery-using-Multi-Agents/prompt/ER_prompt.txt', 'r') as file:
        prompt_template = file.read()
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    multi_query_retriever = MultiQueryRetriever.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=multi_query_retriever,
        memory=memory,
        verbose=True,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

    response = conversation_chain({"question": "Provide a summary based on the prompt template."})

    # Return response and vectorstore
    return response['answer'], vectorstore


if __name__ == "__main__":
    st.title("Record Linkage Using Multi-LLM")

    input_folder = "/Users/aatif/Household-Discovery-using-Multi-Agents/input"
    output_folder = "/Users/aatif/Household-Discovery-using-Multi-Agents/output"
    os.makedirs(output_folder, exist_ok=True)
    available_files = [f for f in os.listdir(input_folder) if f.endswith(('.csv', '.xlsx'))]

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

        # Step 1: Ask user if they want to use the existing vector database
        use_existing_vector = st.radio(
            "Do you want to use the stored vector database?",
            ("Yes, use stored vector database", "No, create a new vector database")
        ) == "Yes, use stored vector database"

        # Step 2: Execute the pipeline
        if st.button("Execute"):
            try:
                combined_response, new_vectorstore = rag_pipeline(
                    selected_files_paths,
                    embedding_model,
                    vector_store,
                    llm_model,
                    use_existing_vector
                )

                # Store the new vectorstore in session state if created
                if not use_existing_vector:
                    st.session_state["new_vectorstore"] = new_vectorstore
                    st.session_state["vectorstore_path"] = "/Users/aatif/Household-Discovery-using-Multi-Agents/stored_vectors/store_index"
                    st.session_state["vectorstore_type"] = vector_store

                # Display the summary
                output_file_path = os.path.join(output_folder, "output_summary.md")
                with open(output_file_path, "w") as output_file:
                    output_file.write(f"# Summary\n\n{combined_response}\n")
                st.success(f"Summary saved to {output_file_path}")
                st.write("## Summary\n", combined_response)

            except Exception as e:
                st.error(f"Error: {e}")

        # Step 3: Prompt to save the vectorstore if it exists in session state
        if "new_vectorstore" in st.session_state:
            save_vector = st.radio(
                "Do you want to save the newly created vector database for future use?",
                ("Yes, save the new vector database", "No, don't save it"),
                index=1  # Default to "No"
            )
            
            if st.button("Save Vectorstore"):
                if save_vector == "Yes, save the new vector database":
                    try:
                        VectorStore.save_local(
                            st.session_state["new_vectorstore"],
                            st.session_state["vectorstore_path"],
                            st.session_state["vectorstore_type"]
                        )
                        st.success(f"New {st.session_state['vectorstore_type']} vector database saved locally at {st.session_state['vectorstore_path']}.")
                        # Clear the saved vectorstore from session state after saving
                        del st.session_state["new_vectorstore"]
                    except Exception as e:
                        st.error(f"Failed to save the new vector database: {e}")
                else:
                    st.info("The new vector database was not saved.")