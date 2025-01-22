![image](https://github.com/user-attachments/assets/959ed9ae-f656-4734-a446-d9c436eb35fe)# AI-Powered Resume Generator

An intelligent resume customization tool that tailors your resume to specific job descriptions using LangGraph and local LLMs.

## 🎯 Overview

This project creates custom-tailored resumes based on job descriptions using local LLMs (Phi-2) through LMStudio. It analyzes both your resume metadata and job descriptions to generate optimized, one-page resumes saved in CSV format.

![image](https://github.com/user-attachments/assets/5c001394-9c78-485d-9415-36a45e3f72a1)


## 🚀 Features

- **Local LLM Integration**: Uses Phi-2 through LMStudio for privacy and cost efficiency
- **Intelligent Matching**: Matches your experience with job requirements
- **Metadata-Based**: Uses structured metadata input instead of PDF parsing
- **Format Control**: Ensures one-page output with proper section formatting
- **CSV Output**: Generates easily editable CSV format
- **LangGraph Workflow**: Structured, maintainable agent-based architecture

## 📋 Project Roadmap

### Phase 1: Core Infrastructure
- [ ] Set up basic project structure
- [ ] Implement LMStudio connection manager
- [ ] Create metadata parser
- [ ] Develop job description parser
- [ ] Set up basic LangGraph workflow

### Phase 2: Agent Development
- [ ] Implement Resume Parser Agent
- [ ] Implement JD Parser Agent
- [ ] Create Matching Agent
- [ ] Develop Section Generator Agents
- [ ] Build Content Assembler

### Phase 3: Output & Validation
- [ ] Implement Format Validator
- [ ] Create Content Trimmer
- [ ] Develop CSV Output Generator
- [ ] Add Length Validation

### Phase 4: Testing & Optimization
- [ ] Create Unit Tests
- [ ] Add Integration Tests
- [ ] Optimize Prompts
- [ ] Performance Testing
- [ ] Error Handling

### Future Enhancements
- [ ] CSV to PDF Converter
- [ ] Multiple Resume Templates
- [ ] Custom Styling Options
- [ ] Multiple LLM Support
- [ ] Web Interface

## 🛠️ Prerequisites

- Python 3.9+
- LMStudio with Phi-2 model
- Required Python packages:
  - langgraph
  - langchain
  - pandas
  - requests
  - pydantic

## 📥 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-resume-generator.git
cd ai-resume-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Unix
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🗂️ Project Structure

```
ai-resume-generator/
├── src/
│   ├── agents/
│   │   ├── resume_parser.py
│   │   ├── jd_parser.py
│   │   ├── matcher.py
│   │   └── section_generator.py
│   ├── utils/
│   │   ├── lmstudio_connection.py
│   │   ├── metadata_parser.py
│   │   └── csv_generator.py
│   └── workflow/
│       └── resume_generator_graph.py
├── tests/
├── examples/
│   ├── metadata_template.txt
│   └── sample_outputs/
├── requirements.txt
└── README.md
```

## 📝 Metadata Format

The metadata should be provided in a structured text file:

```yaml
personal_info:
  name: "John Doe"
  email: "john@example.com"
  location: "City, Country"
  
education:
  - degree: "Bachelor's in Computer Science"
    institution: "University Name"
    year: "2020"
    
experience:
  - title: "Software Engineer"
    company: "Tech Corp"
    duration: "2020-2023"
    highlights:
      - "Developed scalable applications"
      - "Led team of 5 developers"
      
skills:
  technical:
    - "Python"
    - "JavaScript"
  soft:
    - "Leadership"
    - "Communication"
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangGraph team for the workflow framework
- LMStudio for local LLM support
- Phi-2 team for the language model
