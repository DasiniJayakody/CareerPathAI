# 🚀 CareerPathAI - AI-Powered Career Guidance System

CareerPathAI is a comprehensive AI-powered career guidance system that helps job seekers analyze their skills, get personalized career recommendations, and develop learning plans to achieve their career goals.

## ✨ Features

- **📄 Resume Parsing**: Extract skills and information from PDF/DOCX resumes using NLP
- **🎯 Career Recommendations**: Get personalized job recommendations based on your skills
- **🔍 Skill Gap Analysis**: Identify missing skills for your target roles
- **📚 Learning Plans**: Get curated learning resources for skill development
- **💡 Personalized Advice**: Receive tailored career guidance and next steps
- **📊 Skill Visualization**: Interactive charts and metrics for skill analysis
- **🔧 Manual Skills Input**: Don't have a resume? Input skills manually

## 🛠️ Technology Stack

### Backend

- **FastAPI**: Modern, fast web framework for building APIs
- **spaCy**: Advanced NLP for text processing and entity extraction
- **scikit-learn**: Machine learning for clustering and analysis
- **Sentence Transformers**: State-of-the-art text embeddings
- **PDFMiner**: PDF text extraction
- **python-docx**: DOCX file processing

### Frontend

- **Streamlit**: Beautiful, interactive web application
- **Plotly**: Interactive data visualizations
- **Requests**: HTTP client for API communication

### ML/AI

- **NLP**: Named Entity Recognition, skill extraction
- **Clustering**: Career path clustering
- **Similarity Matching**: Skill-to-job matching algorithms

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd CareerPathAI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### 6. Start the Backend Server

```bash
cd app
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 7. Start the Frontend Application

```bash
cd frontend
streamlit run app.py
```

The web app will be available at `http://localhost:8501`

## 📁 Project Structure

```
CareerPathAI/
├── app/
│   ├── main.py                 # FastAPI backend
│   ├── models/                 # ML models (future)
│   ├── services/
│   │   ├── resume_parser.py    # Resume parsing service
│   │   └── career_recommender.py # Career recommendation engine
│   └── utils/                  # Helper utilities
├── frontend/
│   └── app.py                  # Streamlit frontend
├── data/
│   ├── resumes/                # Sample resumes
│   └── jobs/                   # Job data
├── notebooks/                  # Jupyter notebooks for development
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🎯 Usage Guide

### Resume Analysis

1. Open the web application at `http://localhost:8501`
2. Navigate to "Upload Resume" in the sidebar
3. Upload your PDF or DOCX resume
4. View the analysis results:
   - Extracted skills by category
   - Career recommendations with match scores
   - Learning plan for missing skills
   - Personalized career advice

### Manual Skills Input

1. Navigate to "Manual Skills Input" in the sidebar
2. Select your skills from the dropdown menus
3. Click "Analyze Skills"
4. Get the same comprehensive analysis without a resume

## 🔧 API Endpoints

### Core Endpoints

- `GET /`: API information and available endpoints
- `GET /health`: Health check
- `POST /upload_resume`: Upload and parse resume file
- `POST /parse_text`: Parse resume from text input
- `POST /analyze_skills`: Analyze skills without resume

### Information Endpoints

- `GET /job_profiles`: Get available job profiles
- `GET /learning_resources`: Get learning resources

## 📊 Sample Output

### Resume Analysis Results

```json
{
  "parsed_resume": {
    "name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "(555) 123-4567",
    "skills": {
      "programming": ["python", "javascript", "java"],
      "web_development": ["react", "node.js", "django"],
      "databases": ["mysql", "postgresql", "mongodb"],
      "cloud_platforms": ["aws", "docker", "kubernetes"]
    }
  },
  "career_analysis": {
    "recommendations": [
      {
        "job_title": "Software Engineer",
        "match_score": 85.5,
        "description": "Design, develop, and maintain software applications",
        "missing_skills": ["algorithms", "data structures"]
      }
    ],
    "learning_plan": {
      "algorithms": {
        "courses": ["https://www.coursera.org/learn/algorithms"],
        "books": ["Introduction to Algorithms"],
        "practice": ["LeetCode", "HackerRank"]
      }
    }
  }
}
```

## 🎨 Customization

### Adding New Skills

Edit `app/services/resume_parser.py` to add new skill categories:

```python
SKILL_KEYWORDS = {
    'new_category': [
        'skill1', 'skill2', 'skill3'
    ]
}
```

### Adding New Job Profiles

Edit `app/services/career_recommender.py` to add new job profiles:

```python
JOB_PROFILES = {
    'New Job Title': {
        'required_skills': ['skill1', 'skill2'],
        'preferred_skills': ['skill3', 'skill4'],
        'description': 'Job description here'
    }
}
```

### Adding Learning Resources

Update the `LEARNING_RESOURCES` dictionary in `career_recommender.py`:

```python
LEARNING_RESOURCES = {
    'new_skill': {
        'courses': ['course_url'],
        'books': ['book_title'],
        'practice': ['practice_platform']
    }
}
```

## 🚀 Deployment

### Local Development

1. Follow the Quick Start guide above
2. Both backend and frontend will run on localhost

### Production Deployment

1. **Backend**: Deploy to cloud platforms like:

   - Heroku
   - Railway
   - AWS EC2
   - Google Cloud Run

2. **Frontend**: Deploy to:
   - Streamlit Cloud
   - Vercel
   - Netlify

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- spaCy for excellent NLP capabilities
- Streamlit for the beautiful web interface
- FastAPI for the robust backend framework
- The open-source community for inspiration and tools

## 📞 Support

If you encounter any issues or have questions:

1. Check the existing issues
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Made with ❤️ by Dasini Jayakody for job seekers worldwide**
