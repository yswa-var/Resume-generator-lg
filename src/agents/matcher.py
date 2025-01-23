import json
from src.agents.jd_parser import jd_processor, jd_flatten
from src.agents.resume_parser import load_metadata, flatten_metadata
from src.utils.lmstudio_connection import query_lmstudio
from src.utils.metadata_parser import vector_saver, similar_search


def process_skills(query, vector_store, user_query_key):
    """
    A function to perform the search and append results to user_query.
    """
    try:
        results = similar_search(query, vector_store=vector_store)
        user_query[user_query_key] = [str(doc.page_content) for doc in results]
    except Exception as e:
        print(f"Error in processing {user_query_key}: {str(e)}")


# Loading and flattening resume metadata
resume_metadata = load_metadata("/Users/apple/PycharmProjects/Resume-generator-lg/src/metadata/meta_data.yaml")
resume_flatten = flatten_metadata(resume_metadata)

# Loading and processing job description
jd_query = """
Job description

    This is a remote internship role for an Artificial Intelligence Intern
    As an AI Intern, you will be responsible for assisting in the development and implementation of AI models and algorithms
    You will work on data analysis, machine learning, programming, and other tasks related to AI development
    This internship will provide you with valuable hands-on experience in the field of artificial intelligence

Job Requirement

    Computer Science and Programming skills

    Analytical Skills and Data Science knowledge

    Experience or knowledge in Machine Learning

    Excellent problem-solving and critical thinking abilities

    Strong communication and teamwork skills

    Ability to work independently and remotely

    Experience with AI frameworks and tools is a plus

    Currently pursuing or recently completed a degree in Computer Science, Data Science, or a related field

Role: Data Science & Machine Learning - Other
Industry Type: Internet
Department: Data Science & Analytics
Employment Type: Full Time, Permanent
Role Category: Data Science & Machine Learning
Education
UG: Any Graduate
PG: Any Postgraduate
Key Skills
AutomationData analysisLinuxApplication programmingMachine learningPerformance testingInternshipAnalyticsAndroid
"""
response = jd_processor(jd_query)
response_flatten = jd_flatten(response)

# Initialize user query dictionary
user_query = {}

# Process skills in resume
res_vs = vector_saver(resume_flatten, chunk_type="resume")
process_skills("What are listed in the skills?", res_vs, "skills_in_resume")

# Process skills in job description
jd_vs = vector_saver(response_flatten, chunk_type="jd")
process_skills("What programming languages are listed in the skills?", jd_vs, "skills_in_job_description")

# Convert user query to JSON
user_query = json.dumps(user_query)

# Set context (you can modify this as needed to make it meaningful)
# Prompt Template for Comprehensive Skills Analysis
context = """
You are an expert skills extractor and ATS (Applicant Tracking System) optimization specialist. 
Analyze the provided resume and job description to extract and categorize skills comprehensively.

Input:
- Resume Skills
- Job Description 

Tasks:
1. Skills Matching Analysis
   * List ALL skills present in BOTH resume and job description
   * Categorize skills into:
     - Soft Skills
     - Technical Skills
     - Frameworks & Tools
     - Programming Languages
     - Domain-Specific Skills

2. Skills Gap Identification
   * Identify skills in JOB DESCRIPTION NOT FOUND in resume
     - Prioritize these as LEARNING OPPORTUNITIES
     - Rank by importance/frequency in job description

3. ATS Keyword Optimization
   * Extract TOP keywords from job description
   * Rank keywords by:
     - Frequency
     - Potential impact on ATS score
     - Alignment with job requirements

4. Skill Strength Scoring
   * Assign a match percentage for each skill category
   * Recommend specific upskilling strategies

Output Format:
```json
{
  "skills_match": {
    "total_match_percentage": float,
    "matched_skills": {
      "soft_skills": [],
      "technical_skills": [],
      "frameworks_tools": [],
      "programming_languages": []
    }
  },
  "skills_gap": {
    "missing_skills": [
      {
        "skill": str,
        "category": str,
        "priority_score": float,
        "learning_resources": []
      }
    ]
  },
  "ats_keywords": {
    "top_keywords": [
      {
        "keyword": str,
        "frequency": int,
        "ats_impact_score": float
      }
    ]
  }
}
```

Processing Instructions:
- Be case-insensitive during matching
- Consider skill variations and synonyms
- Provide actionable insights
"""

# Query LM Studio
lms_result = query_lmstudio(context=context, user_query=user_query)

print(lms_result)