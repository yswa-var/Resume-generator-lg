from pathlib import Path
from typing import Dict, List
import yaml
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS


class ResumeVectorStore:
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

    def create_vector_store(self, metadata_path: str) -> FAISS:
        """
        Create a FAISS vector store from resume metadata.
        """
        # Load and process metadata
        metadata = self.load_metadata(metadata_path)
        documents = self._flatten_metadata(metadata['meta_data'])

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

    def load_metadata(self, file_path) -> Dict:
        """
        Load metadata from YAML file or directory containing YAML files.
        If a directory is provided, it will load and merge all YAML files.
        """
        path = Path(file_path)

        if path.is_file():
            return yaml.safe_load(path.read_text())
        elif path.is_dir():
            metadata = {}
            yaml_files = list(path.glob('*.yaml')) + list(path.glob('*.yml'))

            if not yaml_files:
                raise FileNotFoundError(f"No YAML files found in directory: {file_path}")

            for yaml_file in yaml_files:
                try:
                    file_data = yaml.safe_load(yaml_file.read_text())
                    if file_data:
                        # Merge data based on the filename (without extension)
                        section_name = yaml_file.stem
                        metadata[section_name] = file_data
                except yaml.YAMLError as e:
                    print(f"Error loading {yaml_file}: {e}")
                    continue

            if not metadata:
                raise ValueError(f"No valid YAML data found in directory: {file_path}")

            return metadata
        else:
            raise FileNotFoundError(f"Path not found: {file_path}")

    def _flatten_metadata(self, metadata: Dict) -> List[str]:
        """Convert nested metadata into flat documents."""
        documents = []

        # Process personal info
        if 'personal_info' in metadata:
            personal_info = metadata['personal_info']
            documents.append(f"Personal Information: Name: {personal_info.get('name')}, "
                             f"Email: {personal_info.get('email')}, "
                             f"Location: {personal_info.get('location')}, "
                             f"GitHub: {personal_info.get('github')}, "
                             f"Phone: {personal_info.get('phone_number')}")

        # Process education
        if 'education' in metadata:
            for edu in metadata['education']:
                edu_text = (f"Education: {edu.get('degree')} in {edu.get('major')} from {edu.get('institution')} "
                            f"({edu.get('graduation_year')}), CGPA: {edu.get('cgpa')}, Minor: {edu.get('minor')}")
                documents.append(edu_text)

        # Process experience
        if 'experience' in metadata:
            for exp in metadata['experience']:
                exp_text = (f"Experience: {exp.get('title')} at {exp.get('company')} "
                            f"({exp.get('duration')}), Location: {exp.get('location')}, "
                            f"Key Skills: {exp.get('key_skills', '')}, Highlights: {', '.join(exp.get('highlights', []))}")
                documents.append(exp_text)

        # Process skills
        if 'skills' in metadata:
            for category, skills in metadata['skills'].items():
                skills_text = f"Skills ({category}): {', '.join(skills)}"
                documents.append(skills_text)

        # Process projects
        if 'projects' in metadata:
            for project in metadata['projects']:
                project_text = (f"Project: {project.get('title')} "
                                f"Link: {project.get('link')}, "
                                f"Description: {project.get('description')}")
                documents.append(project_text)

        # Process certifications, courses, and achievements
        if 'certifications_courses_achievements' in metadata:
            for cca in metadata['certifications_courses_achievements']:
                cca_text = (f"{cca.get('title')} "
                            f"Link: {cca.get('link', '')}, "
                            f"Description: {cca.get('description')}")
                documents.append(cca_text)

            return documents

def main():
    # Initialize vector store manager
    vector_store_manager = ResumeVectorStore()

    try:
        # Create vector store from metadata
        vector_store = vector_store_manager.create_vector_store(
            metadata_path="/Users/yash/PycharmProjects/Resume-generator-lg/src/metadata"
        )

        # Save vector store
        vector_store.save_local("resume_vectorstore")

        # Example search
        query = "What programming languages are listed in the skills?"
        results = vector_store.similarity_search(query)

        print("\nSearch Results:")
        for doc in results:
            print(f"\n{doc.page_content}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()