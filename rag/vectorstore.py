import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS, Qdrant, Chroma

load_dotenv()

class VectorStore:

    @staticmethod
    def get_available_vectorstores():
        return ['faiss', 'qdrant', 'chroma']

    @staticmethod
    def vectorization(store_select, text_chunks, embeddings):
        if store_select.lower() == 'faiss':
            try:
                vectorstore = FAISS.from_texts(
                    texts=text_chunks,
                    embedding=embeddings
                )
            except Exception as e:
                raise Exception(f"Cannot load FAISS vectorstore. Error: {e}")
        
        elif store_select.lower() == 'qdrant':
            try:
                vectorstore = Qdrant.from_texts(
                    texts=text_chunks,
                    url=os.getenv("QDRANT_URL"),
                    api_key=os.getenv("QDRANT_API_KEY"),
                    collection_name=os.getenv("COLLECTION_NAME"),
                    embedding=embeddings
                )
            except Exception as e:
                raise Exception(f"Cannot load Qdrant vectorstore. Error: {e}")
            
        elif store_select.lower() == 'chroma':
            try:
                vectorstore = Chroma.from_texts(
                    texts=text_chunks,
                    embedding=embeddings
                )
            except Exception as e:
                raise Exception(f"Cannot load Chroma vectorstore. Error: {e}")
        
        else:
            raise ValueError("Unsupported vector store type. Choose 'faiss', 'qdrant', or 'chroma'.")
        
        return vectorstore

    @staticmethod
    def save_local(vectorstore, path, store_type):
        """
        Save the vectorstore locally.
        """
        if store_type.lower() == 'faiss':
            vectorstore.save_local(path)
        elif store_type.lower() == 'qdrant':
            raise NotImplementedError("Saving Qdrant locally is not supported. Use the Qdrant server.")
        elif store_type.lower() == 'chroma':
            vectorstore.persist(path)
        else:
            raise ValueError("Unsupported vectorstore type for saving.")

    @staticmethod
    def load_local(path, store_type, embeddings=None):
        """
        Load a vectorstore from a local file.
        """
        if store_type.lower() == 'faiss':
            if embeddings is None:
                raise ValueError("Embeddings must be provided to load a FAISS vectorstore.")
            try:
                vectorstore = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
            except Exception as e:
                raise Exception(f"Cannot load FAISS vectorstore. Error: {e}")
        elif store_type.lower() == 'qdrant':
            raise NotImplementedError("Loading Qdrant locally is not supported. Use the Qdrant server.")
        elif store_type.lower() == 'chroma':
            try:
                vectorstore = Chroma(persist_directory=path)
            except Exception as e:
                raise Exception(f"Cannot load Chroma vectorstore. Error: {e}")
        else:
            raise ValueError("Unsupported vectorstore type for loading.")
        
        return vectorstore
