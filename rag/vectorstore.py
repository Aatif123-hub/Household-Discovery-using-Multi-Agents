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
