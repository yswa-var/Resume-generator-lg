from pathlib import Path
from typing import Dict, List

import yaml

from src.utils.metadata_parser import VectorStore, similar_search, vector_saver


def load_metadata(file_path) -> Dict:
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


def flatten_metadata(metadata: Dict) -> List[str]:
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
    resume_metadata = load_metadata("/Users/apple/PycharmProjects/Resume-generator-lg/src/metadata/meta_data.yaml")
    resume_flatten = flatten_metadata(resume_metadata)

    try:
        res_vs = vector_saver(resume_flatten, chunk_type="resume")

        # Example search
        query = "What programming languages are listed in the skills?"
        results = similar_search(query, vector_store = res_vs)

        print("\nSearch Results:")
        for doc in results:
            print(f"\n{doc.page_content}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()