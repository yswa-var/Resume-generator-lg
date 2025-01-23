# import os
# from pathlib import Path
# from typing import Dict, List, Optional
#
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
#
#
# class VectorStoreManager:
#     def __init__(self,
#                  model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
#                  base_path: str = "src/agents/vector_stores"):
#         """
#         Initialize Vector Store Manager with configurable paths and embeddings
#
#         Args:
#             model_name: Embedding model to use
#             base_path: Base directory to store vector stores
#         """
#         self.embeddings = HuggingFaceEmbeddings(
#             model_name=model_name,
#             model_kwargs={'device': 'cpu'},
#             encode_kwargs={'normalize_embeddings': True}
#         )
#
#         # Ensure base path exists
#         self.base_path = Path(base_path)
#         self.base_path.mkdir(parents=True, exist_ok=True)
#
#         # Define specific store paths
#         self.resume_store_path = self.base_path / "resume_vectorstore"
#         self.jd_store_path = self.base_path / "jd_vectorstore"
#
#         # Create directories if they don't exist
#         self.resume_store_path.mkdir(parents=True, exist_ok=True)
#         self.jd_store_path.mkdir(parents=True, exist_ok=True)
#
#     def create_vector_store(self,
#                             texts: List[str],
#                             store_type: str = 'resume') -> FAISS:
#         """
#         Create a vector store from given texts
#
#         Args:
#             texts: List of text chunks to vectorize
#             store_type: 'resume' or 'jd'
#
#         Returns:
#             FAISS vector store
#         """
#         # Split texts
#         text_splitter = CharacterTextSplitter(
#             chunk_size=500,
#             chunk_overlap=50,
#             separator="\n"
#         )
#
#         chunks = []
#         for text in texts:
#             chunks.extend(text_splitter.split_text(text))
#
#         # Create vector store
#         vector_store = FAISS.from_texts(
#             texts=chunks,
#             embedding=self.embeddings
#         )
#
#         return vector_store
#
#     def save_vector_store(self,
#                           vector_store: FAISS,
#                           store_type: str = 'resume') -> None:
#         """
#         Save vector store to appropriate directory
#
#         Args:
#             vector_store: FAISS vector store to save
#             store_type: 'resume' or 'jd'
#         """
#         store_path = self.resume_store_path if store_type == 'resume' else self.jd_store_path
#         vector_store.save_local(str(store_path))
#
#     def load_vector_store(self,
#                           store_type: str = 'resume') -> Optional[FAISS]:
#         """
#         Load vector store from appropriate directory
#
#         Args:
#             store_type: 'resume' or 'jd'
#
#         Returns:
#             Loaded FAISS vector store or None
#         """
#         store_path = self.resume_store_path if store_type == 'resume' else self.jd_store_path
#
#         try:
#             return FAISS.load_local(str(store_path), self.embeddings)
#         except Exception as e:
#             print(f"Error loading vector store: {e}")
#             return None
#
#     def search_vector_store(self,
#                             query: str,
#                             store_type: str = 'resume',
#                             k: int = 3) -> List[str]:
#         """
#         Perform similarity search on a vector store
#
#         Args:
#             query: Search query
#             store_type: 'resume' or 'jd'
#             k: Number of results to return
#
#         Returns:
#             List of most similar text chunks
#         """
#         vector_store = self.load_vector_store(store_type)
#
#         if vector_store is None:
#             return []
#
#         results = vector_store.similarity_search(query, k=k)
#         return [doc.page_content for doc in results]
#
#
# def prepare_jd_vector_store(jd_processor_output: Dict) -> None:
#     """
#     Prepare vector store for job description
#
#     Args:
#         jd_processor_output: Dictionary output from jd_processor
#     """
#     # Convert JD dict to list of strings for vectorization
#     jd_texts = []
#
#     # Add various JD components to texts
#     for key, value in jd_processor_output.items():
#         if isinstance(value, list):
#             jd_texts.extend([str(item) for item in value])
#         else:
#             jd_texts.append(str(value))
#
#     # Create vector store manager
#     vs_manager = VectorStoreManager()
#
#     # Create and save JD vector store
#     jd_vector_store = vs_manager.create_vector_store(jd_texts, store_type='jd')
#     vs_manager.save_vector_store(jd_vector_store, store_type='jd')
#
#
# def example_matcher_workflow():
#     """
#     Example workflow showing how to use vector stores in matcher
#     """
#     # Initialize Vector Store Manager
#     vs_manager = VectorStoreManager()
#
#     # Load Resume Vector Store
#     resume_store = vs_manager.load_vector_store(store_type='resume')
#
#     # Load Job Description Vector Store
#     jd_store = vs_manager.load_vector_store(store_type='jd')
#
#     # Perform similarity searches
#     resume_context = vs_manager.search_vector_store(
#         "Find skills related to software engineering",
#         store_type='resume'
#     )
#
#     jd_context = vs_manager.search_vector_store(
#         "Software engineering skills required",
#         store_type='jd'
#     )
#
#     # Use contexts for matching or further processing
#     print("Resume Context:", resume_context)
#     print("JD Context:", jd_context)
#
#
# if __name__ == "__main__":
#     # Example usage in jd_parser.py
#     # from jd_processor import process_job_description
#     # jd_output = process_job_description(job_description)
#     # prepare_jd_vector_store(jd_output)
#
#     example_matcher_workflow()

from pathlib import Path
from typing import Dict, List
import yaml
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS


def similar_search(query, vector_store):
    results = vector_store.similarity_search(query)
    return results


def vector_saver(chunks, chunk_type ="resume"):
    # Initialize vector store manager
    vector_store_manager = VectorStore()

    try:
        if chunk_type == "resume":
            resume_vector_store = vector_store_manager.create_vector_store(flatten_data=chunks)
            resume_vector_store.save_local("vector_stores/resume_vectorstore")
            return resume_vector_store
        else:
            jd_vector_store = vector_store_manager.create_vector_store(flatten_data=chunks)
            jd_vector_store.save_local("vector_stores/jd_vectorstore")
            return jd_vector_store

        # Example search
    except Exception as e:
        print(f"Error: {str(e)}")


class VectorStore:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the vector store with specified embedding model.
        Uses a lightweight model by default that can run locally.
        """
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.text_splitter = CharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separator="\n"
        )

    def create_vector_store(self, flatten_data: List[str]) -> FAISS:
        """
        Create a FAISS vector store from resume metadata.
        """
        # Load and process metadata
        documents = flatten_data

        if not documents:
            raise ValueError("No valid documents generated from metadata")

        # Split into chunks
        chunks = []
        for doc in documents:
            chunks.extend(self.text_splitter.split_text(doc))

        # Create FAISS vector store using langchain's implementation
        vector_store = FAISS.from_texts(
            texts=chunks,
            embedding=self.embeddings
        )

        return vector_store
