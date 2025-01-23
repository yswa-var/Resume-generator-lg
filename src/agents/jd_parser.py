from src.utils.lmstudio_connection import query_lmstudio
import json

from src.utils.metadata_parser import VectorStore, similar_search, vector_saver


def convert_string_to_json(json_string):
    # Remove the leading and trailing '```json' and '\n'
    clean_json_string = json_string.strip('```json\n').strip()

    # Load the JSON string into a Python dictionary
    json_data = json.loads(clean_json_string)

    return json_data

def jd_processor(user_query) -> dict:
    context = """
    Please review the job description and extract the necessary information to create a structured JSON object. Follow the structure provided and ensure that if any specific information is not mentioned in the job description, it is set appropriately as indicated.
    
    **Structured JSON Format:**
    
    ```json
    {
      "required_experience": "if there is no mention of required experience, set it to '0 years'",
      "required_skills": [
        "example1",
        "example2",
        "example3"
        // Add more skills as extracted from the job description
      ],
      "company_name": "[Extract company name from job description]",
      "job_description": [
        "small and concise points summarizing the role",
        "example1",
        "example2"
        // Add more key points as extracted from the job description
      ]
    }
    ```
    
    **Instructions:**
    
    1. **Company Name:** Extract the name of the company offering the job.
       
    2. **Required Experience:** Look for any mention of required experience in years or other terms. If none is mentioned, set it to "0 years".
    
    3. **Required Skills:** Identify and list all the skills that are mentioned as necessary for the role.
    
    4. **Job Description:** Summarize the main responsibilities and key points of the job into small, concise statements.
    
    ---
    
    **Example:**
    
    Suppose the job description is:
    
    "XYZ Corp is hiring a Software Engineer with 3+ years of experience in Python and Java. The ideal candidate should have strong problem-solving skills and experience with cloud platforms like AWS. Responsibilities include developing scalable applications and collaborating with cross-functional teams."
    
    The structured JSON would be:
    
    ```json
    {
      "required_experience": "3+ years",
      "required_skills": [
        "Python",
        "Java",
        "problem-solving skills",
        "AWS"
      ],
      "company_name": "XYZ Corp",
      "job_description": [
        "Develop scalable applications",
        "Collaborate with cross-functional teams"
      ]
    }
    ```
    
    Use this format to convert any job description into the desired JSON structure.
    only provide the json no other text or explanation is required
    
    """
    lms_result = query_lmstudio(context=context, user_query=user_query)
    result = convert_string_to_json(lms_result)
    return result

def jd_flatten(data):
    documents = []

    # Process personal info
    if 'required_experience' in data:
        documents.append(f"data: {data.get('required_experience')}")

    if 'required_skills' in data:
        skills_text = f"required_skills: ({', '.join(data['required_skills'])}"
        documents.append(skills_text)

    if 'company_name' in data:
        company_name = data['company_name']
        documents.append(f"company_name: {company_name}")


    if 'job_description' in data:
        job_description_txt = f"job_description: ({', '.join(data['job_description'])}"
        documents.append(job_description_txt)

    return documents


def main():
    # Initialize vector store manager
    jd_query = """
    Job description
Job Summary
As an Artificial Intelligence Engineer at WN Infotech, you will be responsible for developing, implementing, and maintaining AI solutions to enhance our products and services. You will work closely with our software development and data science teams to design and deploy cutting-edge AI algorithms and models. This role offers an exciting opportunity to work on innovative projects and contribute to the advancement of AI technology within our organization.
Your Role and Responsibilities
    Develop AI models and algorithms to solve complex business problems and enhance product functionality.
    Collaborate with software development and data science teams to integrate AI capabilities into existing systems and applications.
    Research and implement state-of-the-art AI techniques and technologies to improve the performance and efficiency of our AI solutions.
    Evaluate and optimize AI models for performance, scalability, and accuracy.
    Stay up-to-date with the latest developments in AI and machine learning by attending conferences, participating in workshops, and engaging with the AI community.
Required Technical and Professional Expertise
    Proficiency in programming languages such as Python, Java, or C++.
    Strong understanding of machine learning algorithms and techniques, including deep learning, reinforcement learning, and natural language processing.
    Experience with AI development frameworks and libraries such as TensorFlow, PyTorch, or Keras.
    Solid understanding of software development principles and best practices.
    Excellent problem-solving skills and attention to detail.
Qualification & Experience Required
    Bachelor's degree or higher in Computer Science, Engineering, Mathematics, or a related field.
    Proven experience in developing and deploying AI solutions in a production environment.
    Experience with big data technologies such as Hadoop, Spark, or Kafka is a plus.
    Strong analytical and mathematical skills.
    Ability to work effectively in a fast-paced and collaborative team environment.
Role: Machine Learning Engineer
Industry Type: Software Product
Department: Data Science & Analytics
Employment Type: Full Time, Permanent
Role Category: Data Science & Machine Learning
Education
UG: Any Graduate
PG: Any Postgraduate
Key Skills
Computer science deep learning C++ data science Analytical Artificial Intelligence Machine learning Natural language processing big data Python
    """
    response = jd_processor(jd_query)
    response_flatten = jd_flatten(response)

    try:
        jd_vs = vector_saver(response_flatten, chunk_type="jd")

        # Example search
        query = "What programming languages are listed in the skills?"
        results = similar_search(query, vector_store = jd_vs)

        print("\nSearch Results:")
        for doc in results:
            print(f"\n{doc.page_content}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()