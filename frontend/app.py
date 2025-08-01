import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import base64

# Page configuration
st.set_page_config(
    page_title="CareerPathAI - Multi-Sector Career Guidance",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        color: #2c3e50;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    .sector-card {
        background-color: #ffffff;
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .job-card {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .skill-tag {
        background-color: #007bff;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.25rem;
        display: inline-block;
    }
    .sector-tag {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.25rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000"

# Define sectors for filtering
SECTORS = {
    'technology': 'Technology & IT',
    'healthcare': 'Healthcare',
    'finance': 'Finance',
    'education': 'Education',
    'marketing': 'Marketing & Sales',
    'legal': 'Legal',
    'engineering': 'Engineering',
    'hospitality': 'Hospitality & Tourism',
    'government': 'Government & Public Sector',
    'nonprofit': 'Non-Profit',
    'manufacturing': 'Manufacturing',
    'retail': 'Retail',
    'business': 'Business & Management'
}

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_resume_api(file):
    """Upload resume to API"""
    try:
        files = {"file": file}
        response = requests.post(f"{API_BASE_URL}/upload_resume", files=files)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error uploading resume: {str(e)}")
        return None

def analyze_skills_api(skills_data):
    """Analyze skills via API"""
    try:
        response = requests.post(f"{API_BASE_URL}/analyze_skills", json=skills_data)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error analyzing skills: {str(e)}")
        return None

def display_skill_analysis(skill_analysis: Dict):
    """Display skill analysis metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Skills", skill_analysis.get('total_skills', 0))
    
    with col2:
        st.metric("Skill Categories", len(skill_analysis.get('skill_categories', [])))
    
    with col3:
        strongest = skill_analysis.get('strongest_category', 'N/A')
        st.metric("Strongest Area", strongest.replace('_', ' ').title())
    
    with col4:
        diversity_score = skill_analysis.get('skill_diversity_score', 0)
        st.metric("Diversity Score", f"{diversity_score:.1%}")

def display_recommendations(recommendations: List[Dict]):
    """Display career recommendations"""
    st.subheader("🎯 Career Recommendations")
    
    for i, rec in enumerate(recommendations[:5]):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {i+1}. {rec['job_title']}")
                st.markdown(f"**Match Score:** {rec['match_score']}%")
                st.markdown(f"**Description:** {rec['description']}")
                
                if rec['missing_skills']:
                    st.markdown("**Missing Skills:**")
                    for skill in rec['missing_skills'][:5]:
                        st.markdown(f"• {skill}")
            
            with col2:
                # Create a progress bar for match score
                progress = rec['match_score'] / 100
                st.progress(progress)
                st.markdown(f"**{rec['match_score']}%**")
        
        st.divider()

def display_learning_plan(learning_plan: Dict):
    """Display learning plan for missing skills"""
    if not learning_plan:
        return
    
    st.subheader("📚 Learning Plan")
    
    for skill, resources in learning_plan.items():
        with st.expander(f"Learn {skill}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Courses:**")
                for course in resources.get('courses', [])[:2]:
                    st.markdown(f"• [{course.split('/')[-1]}]({course})")
            
            with col2:
                st.markdown("**Books:**")
                for book in resources.get('books', [])[:2]:
                    st.markdown(f"• {book}")
            
            with col3:
                st.markdown("**Practice:**")
                for practice in resources.get('practice', [])[:2]:
                    st.markdown(f"• {practice}")

def display_personalized_advice(advice: Dict):
    """Display personalized career advice"""
    st.subheader("💡 Personalized Advice")
    
    st.markdown(f"**{advice.get('current_position', '')}**")
    
    if advice.get('next_steps'):
        st.markdown("**Next Steps:**")
        for step in advice['next_steps']:
            st.markdown(f"• {step}")
    
    if advice.get('market_insights'):
        st.markdown("**Market Insights:**")
        for insight in advice['market_insights']:
            st.markdown(f"• {insight}")
    
    if advice.get('skill_gaps'):
        st.markdown("**Skill Development:**")
        for gap in advice['skill_gaps']:
            st.markdown(f"• {gap}")

def create_skill_chart(skills: Dict[str, List[str]]):
    """Create a chart showing skill distribution"""
    if not skills:
        return None
    
    # Flatten skills and count by category
    skill_counts = {}
    for category, skill_list in skills.items():
        skill_counts[category.replace('_', ' ').title()] = len(skill_list)
    
    if not skill_counts:
        return None
    
    fig = px.bar(
        x=list(skill_counts.keys()),
        y=list(skill_counts.values()),
        title="Skill Distribution by Category",
        labels={'x': 'Skill Category', 'y': 'Number of Skills'}
    )
    fig.update_layout(height=400)
    return fig

def main():
    st.markdown('<h1 class="main-header">🚀 CareerPathAI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Multi-Sector AI-Powered Career Guidance System</p>', unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ Backend API is not running. Please start the backend server first.")
        st.info("To start the backend: `cd app && uvicorn main:app --reload`")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose an option:", ["Upload Resume", "Manual Skills Input", "Sector Explorer", "About"])
    
    if page == "Upload Resume":
        upload_resume_page()
    elif page == "Manual Skills Input":
        manual_skills_page()
    elif page == "Sector Explorer":
        sector_explorer_page()
    elif page == "About":
        about_page()

def upload_resume_page():
    st.markdown('<h2 class="sub-header">📄 Upload Your Resume</h2>', unsafe_allow_html=True)
    
    # Sector filter
    st.sidebar.markdown("### 🎯 Sector Filter")
    selected_sectors = st.sidebar.multiselect(
        "Choose sectors to focus on:",
        options=list(SECTORS.keys()),
        default=[],
        format_func=lambda x: SECTORS[x]
    )
    
    uploaded_file = st.file_uploader(
        "Choose a resume file (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Upload your resume to get personalized career recommendations"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        if st.button("🚀 Analyze Resume", type="primary"):
            with st.spinner("Analyzing your resume..."):
                try:
                    # Upload file to API
                    files = {"file": uploaded_file}
                    response = requests.post(f"{API_BASE_URL}/upload_resume", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        display_results(data, selected_sectors)
                    else:
                        st.error(f"Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error analyzing resume: {str(e)}")

def manual_skills_page():
    st.markdown('<h2 class="sub-header">✍️ Manual Skills Input</h2>', unsafe_allow_html=True)
    
    # Sector filter
    st.sidebar.markdown("### 🎯 Sector Filter")
    selected_sectors = st.sidebar.multiselect(
        "Choose sectors to focus on:",
        options=list(SECTORS.keys()),
        default=[],
        format_func=lambda x: SECTORS[x]
    )
    
    st.markdown("""
    <div class="info-box">
        <strong>💡 Tip:</strong> Enter your skills manually to get career recommendations. 
        You can select from predefined skill categories or add your own skills.
    </div>
    """, unsafe_allow_html=True)
    
    # Skill categories
    skill_categories = {
        'Technology': ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'machine learning'],
        'Healthcare': ['patient care', 'medical terminology', 'cpr', 'medication administration'],
        'Finance': ['financial analysis', 'excel', 'accounting', 'risk management'],
        'Education': ['teaching', 'curriculum development', 'classroom management'],
        'Marketing': ['digital marketing', 'social media', 'seo', 'sales'],
        'Legal': ['legal research', 'contract law', 'litigation'],
        'Engineering': ['autocad', 'solidworks', 'structural analysis'],
        'Hospitality': ['hospitality management', 'customer service', 'cooking techniques'],
        'Government': ['policy research', 'public administration', 'stakeholder engagement'],
        'Non-Profit': ['fundraising', 'grant writing', 'volunteer coordination'],
        'Manufacturing': ['lean manufacturing', 'quality control', 'six sigma'],
        'Retail': ['retail management', 'visual merchandising', 'inventory control'],
        'Business': ['project management', 'leadership', 'communication']
    }
    
    # Manual skill input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Select Skills by Category")
        selected_skills = []
        
        for category, skills in skill_categories.items():
            if st.checkbox(f"**{category}**", key=f"cat_{category}"):
                category_skills = st.multiselect(
                    f"Select {category} skills:",
                    options=skills,
                    key=f"skills_{category}"
                )
                selected_skills.extend(category_skills)
    
    with col2:
        st.markdown("### ✏️ Add Custom Skills")
        custom_skills = st.text_area(
            "Enter additional skills (one per line):",
            height=200,
            help="Enter any additional skills not listed above"
        )
        
        if custom_skills:
            custom_skills_list = [skill.strip() for skill in custom_skills.split('\n') if skill.strip()]
            selected_skills.extend(custom_skills_list)
    
    if st.button("🚀 Get Career Recommendations", type="primary"):
        if selected_skills:
            with st.spinner("Generating recommendations..."):
                try:
                    # Prepare skills data
                    skills_data = {
                        "skills": {
                            "programming": [s for s in selected_skills if s in skill_categories.get('Technology', [])],
                            "healthcare": [s for s in selected_skills if s in skill_categories.get('Healthcare', [])],
                            "finance": [s for s in selected_skills if s in skill_categories.get('Finance', [])],
                            "education": [s for s in selected_skills if s in skill_categories.get('Education', [])],
                            "marketing": [s for s in selected_skills if s in skill_categories.get('Marketing', [])],
                            "legal": [s for s in selected_skills if s in skill_categories.get('Legal', [])],
                            "engineering": [s for s in selected_skills if s in skill_categories.get('Engineering', [])],
                            "hospitality": [s for s in selected_skills if s in skill_categories.get('Hospitality', [])],
                            "government": [s for s in selected_skills if s in skill_categories.get('Government', [])],
                            "nonprofit": [s for s in selected_skills if s in skill_categories.get('Non-Profit', [])],
                            "manufacturing": [s for s in selected_skills if s in skill_categories.get('Manufacturing', [])],
                            "retail": [s for s in selected_skills if s in skill_categories.get('Retail', [])],
                            "business": [s for s in selected_skills if s in skill_categories.get('Business', [])]
                        }
                    }
                    
                    # Send to API
                    response = requests.post(f"{API_BASE_URL}/analyze_skills", json=skills_data)
                    
                    if response.status_code == 200:
                        data = response.json()
                        # For manual skills input, we need to restructure the data
                        # to match what display_results expects
                        restructured_data = {
                            "parsed_resume": {
                                "name": "Manual Skills User",
                                "email": "",
                                "phone": "",
                                "skills": data.get("input_skills", {}).get("skills", {})
                            },
                            "career_analysis": data.get("career_analysis", {})
                        }
                        display_results(restructured_data, selected_sectors)
                    else:
                        st.error(f"Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error generating recommendations: {str(e)}")
        else:
            st.warning("Please select at least one skill to get recommendations.")

def sector_explorer_page():
    st.markdown('<h2 class="sub-header">🌍 Sector Explorer</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>🔍 Explore Career Opportunities:</strong> Discover job profiles and requirements across different sectors.
    </div>
    """, unsafe_allow_html=True)
    
    # Get job profiles from API
    try:
        response = requests.get(f"{API_BASE_URL}/job_profiles")
        if response.status_code == 200:
            data = response.json()
            job_profiles = data.get('job_profiles', {})
            
            # Filter by selected sectors
            selected_sectors = st.multiselect(
                "Select sectors to explore:",
                options=list(SECTORS.keys()),
                default=[],
                format_func=lambda x: SECTORS[x]
            )
            
            if selected_sectors:
                # Convert job_profiles dict to list and filter by sectors
                all_profiles = []
                for profile_id, profile_data in job_profiles.items():
                    profile_data['id'] = profile_id  # Add the profile ID
                    all_profiles.append(profile_data)
                
                filtered_profiles = [
                    profile for profile in all_profiles 
                    if profile.get('sector') in selected_sectors
                ]
                
                st.markdown(f"### 📊 Found {len(filtered_profiles)} job profiles")
                
                # Display job profiles by sector
                for sector in selected_sectors:
                    sector_profiles = [p for p in filtered_profiles if p.get('sector') == sector]
                    if sector_profiles:
                        st.markdown(f'<h3 class="sector-tag">{SECTORS[sector]}</h3>', unsafe_allow_html=True)
                        
                        for profile in sector_profiles:
                            with st.container():
                                st.markdown(f"""
                                <div class="job-card">
                                    <h4>💼 {profile['title']}</h4>
                                    <p><strong>Description:</strong> {profile['description']}</p>
                                    <p><strong>Required Skills:</strong></p>
                                    <div>
                                        {''.join([f'<span class="skill-tag">{skill}</span>' for skill in profile.get('required_skills', [])])}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
            else:
                st.info("Please select at least one sector to explore job profiles.")
        else:
            st.error("Failed to load job profiles")
            
    except Exception as e:
        st.error(f"Error loading sector information: {str(e)}")

def display_results(data, selected_sectors):
    """Display analysis results with sector filtering"""
    
    # Handle API response structure
    if 'parsed_resume' in data:
        # API response from resume upload/parse
        parsed_data = data.get('parsed_resume', {})
        career_analysis = data.get('career_analysis', {})
        
        # Extract data from nested structure
        personal_info = parsed_data
        skills_data = parsed_data.get('skills', {})
        recommendations = career_analysis.get('recommendations', [])
        skill_analysis = career_analysis.get('skill_analysis', {})
        learning_plan = career_analysis.get('learning_plan', {})
        personalized_advice = career_analysis.get('personalized_advice', {})
    else:
        # Direct data (for manual skills input)
        personal_info = data
        skills_data = data.get('skills', {})
        recommendations = data.get('recommendations', [])
        skill_analysis = data.get('skill_analysis', {})
        learning_plan = data.get('learning_plan', {})
        personalized_advice = data.get('personalized_advice', {})
    
    # Filter recommendations by selected sectors
    if selected_sectors:
        recommendations = [
            rec for rec in recommendations 
            if any(sector in rec.get('sector', '').lower() for sector in selected_sectors)
        ]
    
    # Personal Information
    if personal_info.get('name'):
        st.markdown('<h3 class="sub-header">👤 Personal Information</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Name", personal_info.get('name', 'Not found'))
        with col2:
            st.metric("Email", personal_info.get('email', 'Not found'))
        with col3:
            st.metric("Phone", personal_info.get('phone', 'Not found'))
    
    # Extracted Skills
    if skills_data:
        st.markdown('<h3 class="sub-header">🔧 Extracted Skills</h3>', unsafe_allow_html=True)
        
        for category, skills in skills_data.items():
            if skills:
                st.markdown(f"**{category.replace('_', ' ').title()}:**")
                skill_tags = ''.join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
                st.markdown(f'<div>{skill_tags}</div>', unsafe_allow_html=True)
                st.markdown("---")
    
    # Career Recommendations
    if recommendations:
        st.markdown('<h3 class="sub-header">🎯 Career Recommendations</h3>', unsafe_allow_html=True)
        
        # Create metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Recommendations", len(recommendations))
        with col2:
            avg_score = sum(float(rec.get('match_score', 0)) for rec in recommendations) / len(recommendations)
            st.metric("Average Match Score", f"{avg_score:.1f}%")
        with col3:
            sectors = set(rec.get('sector', 'Unknown') for rec in recommendations)
            st.metric("Sectors Covered", len(sectors))
        with col4:
            top_score = max(float(rec.get('match_score', 0)) for rec in recommendations)
            st.metric("Best Match", f"{top_score:.1f}%")
        
        # Display recommendations
        for i, rec in enumerate(recommendations[:5]):  # Show top 5
            with st.container():
                st.markdown(f"""
                <div class="job-card">
                    <h4>#{i+1} {rec['job_title']} - {rec['match_score']}% match</h4>
                    <p><strong>Sector:</strong> <span class="sector-tag">{rec.get('sector', 'Unknown').title()}</span></p>
                    <p><strong>Description:</strong> {rec['description']}</p>
                    {f'<p><strong>Missing Skills:</strong> {", ".join(rec.get("missing_skills", []))}</p>' if rec.get("missing_skills") else ''}
                </div>
                """, unsafe_allow_html=True)
    
    # Skill Analysis
    if skill_analysis:
        st.markdown('<h3 class="sub-header">📊 Skill Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Skill diversity chart
            if 'skill_categories' in skill_analysis and skill_analysis['skill_categories']:
                # Create a chart showing skills by category
                categories = []
                counts = []
                
                # Get skills data from the parsed resume
                if 'parsed_resume' in data:
                    skills_data = data['parsed_resume'].get('skills', {})
                else:
                    skills_data = data.get('skills', {})
                
                for category, skills in skills_data.items():
                    if skills:
                        categories.append(category.replace('_', ' ').title())
                        counts.append(len(skills))
                
                if categories:
                    fig = px.bar(
                        x=categories, 
                        y=counts,
                        title="Skills by Category",
                        labels={'x': 'Category', 'y': 'Number of Skills'}
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No skills data available for chart")
            else:
                st.info("No skill categories available for analysis")
        
        with col2:
            # Metrics
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Skills", skill_analysis.get('total_skills', 0))
            st.metric("Skill Categories", len(skill_analysis.get('skill_categories', [])))
            st.metric("Diversity Score", f"{skill_analysis.get('skill_diversity_score', 0):.1%}")
            st.metric("Strongest Area", skill_analysis.get('strongest_category', 'N/A').replace('_', ' ').title())
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Learning Plan
    if learning_plan:
        st.markdown('<h3 class="sub-header">📚 Learning Plan</h3>', unsafe_allow_html=True)
        
        for skill, resources in learning_plan.items():
            with st.expander(f"📖 {skill.title()}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**🎓 Courses:**")
                    for course in resources.get('courses', []):
                        st.markdown(f"• {course}")
                
                with col2:
                    st.markdown("**📚 Books:**")
                    for book in resources.get('books', []):
                        st.markdown(f"• {book}")
                
                with col3:
                    st.markdown("**💻 Practice:**")
                    for practice in resources.get('practice', []):
                        st.markdown(f"• {practice}")
    
    # Personalized Advice
    if personalized_advice:
        st.markdown('<h3 class="sub-header">💡 Personalized Advice</h3>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="success-box">
            <h4>🎯 Career Assessment</h4>
            <p>{personalized_advice.get('current_position', 'No assessment available.')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if 'next_steps' in personalized_advice:
            st.markdown("**📋 Next Steps:**")
            for step in personalized_advice['next_steps']:
                st.markdown(f"• {step}")
        
        if 'market_insights' in personalized_advice and personalized_advice['market_insights']:
            st.markdown("**📈 Market Insights:**")
            for insight in personalized_advice['market_insights']:
                st.markdown(f"• {insight}")

def about_page():
    st.markdown('<h2 class="sub-header">ℹ️ About CareerPathAI</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>🚀 Multi-Sector Career Guidance System</h3>
        <p>CareerPathAI is an advanced AI-powered career guidance system that helps individuals across all sectors 
        find their ideal career path. Our system analyzes resumes and skills to provide personalized recommendations 
        for jobs in technology, healthcare, finance, education, marketing, legal, engineering, hospitality, 
        government, non-profit, manufacturing, retail, and business sectors.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌍 Supported Sectors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        for sector, name in list(SECTORS.items())[:7]:
            st.markdown(f"• **{name}**")
    
    with col2:
        for sector, name in list(SECTORS.items())[7:]:
            st.markdown(f"• **{name}**")
    
    st.markdown("### 🔧 Key Features")
    st.markdown("""
    - **Resume Parsing**: Extract skills and information from PDF/DOCX resumes
    - **Multi-Sector Analysis**: Support for 13 different industry sectors
    - **Skill Gap Detection**: Identify missing skills for target positions
    - **Personalized Learning Plans**: Customized resources for skill development
    - **Career Recommendations**: AI-powered job matching across sectors
    - **Market Insights**: Current industry trends and demand analysis
    """)
    
    st.markdown("### 🛠️ Technology Stack")
    st.markdown("""
    - **Backend**: FastAPI, Python, Machine Learning
    - **Frontend**: Streamlit, Plotly for visualizations
    - **NLP**: spaCy for text processing and skill extraction
    - **ML**: Sentence Transformers for semantic analysis
    - **Document Processing**: PDF and DOCX parsing
    """)

if __name__ == "__main__":
    main() 