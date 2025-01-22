from src.utils.lmstudio_connection import query_lmstudio
import json


def convert_string_to_json(json_string):
    # Remove the leading and trailing '```json' and '\n'
    clean_json_string = json_string.strip('```json\n').strip()

    # Load the JSON string into a Python dictionary
    json_data = json.loads(clean_json_string)

    return json_data

def jd_processor(user_query):
    context = """
    Please review the job description below and extract the necessary information to create a structured JSON object. Follow the structure provided and ensure that if any specific information is not mentioned in the job description, it is set appropriately as indicated.
    
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

#### test ####
# user_query = """
#         About the job
#     Quantitative Developer (Python)
#
#     Location: Bangalore
#
#     Experience: 2-5 Years
#
#     Team: Enterprise Risk Technology
#
#     About The Role
#
#     Millennium is a top tier global hedge fund with a strong commitment to leveraging innovations in technology and data science to solve complex problems for the business.
#
#     The Enterprise Risk Technology team is looking for Quantitative Developer. The developer will leverage Python, FastAPI/Django, AWS, and data manipulation libraries to provide data-driven solutions to stakeholders.
#
#     Responsibilities
#
#     Work closely with quants, risk managers and other technologists in New York, London and Singapore to develop multi-asset analytics, stress and VaR for our in-house risk platform
#     Develop micro-services using Python and analyze data with pandas/polars.
#     Create and manage cloud applications on AWS.
#     Utilize GIT and appropriate DBMS solutions
#
#     Required Skills/experience
#
#     Strong analytical skills & problem solving capabilities
#     Experience working with python, and data analysis libraries (Pandas/Polars)
#     Experience with REST APIs and cloud services
#     Relational SQL database development experience
#     Unix/Linux command-line experience
#
#     Desirable Skills/experience
#
#     AWS cloud services: EC2, S3, Aurora, Redshift, etc
#     Identity and Access Management: Kerberos, OAuth 2.0, LDAP
#     Broad understanding of financial services instruments.
#     Bachelor’s degree in Computer Science & Engineering from Tier 1 colleges.
#     """
# jd_processor(user_query)