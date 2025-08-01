import spacy
import re
from typing import Dict, List, Optional
from pdfminer.high_level import extract_text
from docx import Document
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define skill keywords for different domains across all sectors
SKILL_KEYWORDS = {
    # Technology & IT Skills
    'programming': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'swift', 'kotlin', 'scala', 'matlab', 'sas', 'stata', 'spss'
    ],
    'web_development': [
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
        'spring', 'asp.net', 'laravel', 'wordpress', 'drupal', 'jquery', 'bootstrap'
    ],
    'databases': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'mariadb',
        'cassandra', 'neo4j', 'elasticsearch', 'dynamodb'
    ],
    'cloud_platforms': [
        'aws', 'azure', 'gcp', 'google cloud', 'amazon web services', 'docker', 'kubernetes',
        'terraform', 'jenkins', 'gitlab', 'github actions'
    ],
    'data_science': [
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'jupyter', 'spark',
        'hadoop', 'hive', 'kafka', 'airflow', 'tableau', 'power bi'
    ],
    'devops': [
        'ci/cd', 'continuous integration', 'continuous deployment', 'jenkins', 'gitlab ci',
        'github actions', 'docker', 'kubernetes', 'terraform', 'ansible', 'chef', 'puppet'
    ],
    
    # Healthcare Skills
    'healthcare': [
        'patient care', 'medical terminology', 'clinical skills', 'cpr', 'medication administration',
        'electronic health records', 'iv therapy', 'wound care', 'medical diagnosis', 'anatomy',
        'pharmacy', 'drug interactions', 'prescription', 'physical therapy', 'rehabilitation',
        'patient assessment', 'treatment planning', 'specialized techniques', 'sports medicine'
    ],
    
    # Finance & Business Skills
    'finance': [
        'financial analysis', 'excel', 'financial modeling', 'accounting', 'budgeting',
        'bloomberg terminal', 'risk management', 'investment analysis', 'bookkeeping',
        'tax preparation', 'financial reporting', 'quickbooks', 'audit', 'cpa certification',
        'valuation', 'corporate finance', 'mergers acquisitions', 'regulatory compliance',
        'insurance', 'enterprise risk management'
    ],
    
    # Education Skills
    'education': [
        'teaching', 'curriculum development', 'classroom management', 'communication',
        'lesson planning', 'technology integration', 'special education', 'bilingual',
        'assessment', 'research', 'academic writing', 'subject expertise', 'publication',
        'grant writing', 'mentoring', 'conference presentation', 'peer review',
        'leadership', 'budget management', 'staff supervision', 'education policy',
        'strategic planning', 'community relations', 'crisis management'
    ],
    
    # Marketing & Sales Skills
    'marketing': [
        'marketing strategy', 'digital marketing', 'analytics', 'project management',
        'brand management', 'social media', 'content creation', 'seo', 'market research',
        'sales techniques', 'customer relationship management', 'negotiation', 'product knowledge',
        'crm software', 'territory management', 'closing', 'lead generation', 'email marketing',
        'google ads', 'content marketing', 'automation tools', 'conversion optimization',
        'influencer marketing'
    ],
    
    # Legal Skills
    'legal': [
        'legal research', 'contract law', 'litigation', 'legal writing', 'client counseling',
        'specialized practice areas', 'negotiation', 'courtroom experience', 'mediation',
        'document preparation', 'case management', 'legal terminology', 'court filing',
        'litigation support', 'trial preparation', 'legal software'
    ],
    
    # Engineering Skills
    'engineering': [
        'autocad', 'structural analysis', 'project management', 'engineering design',
        'construction', 'bim modeling', 'sustainability', 'construction management',
        'geotechnical', 'solidworks', 'mechanical design', 'thermodynamics', 'materials science',
        'manufacturing', '3d modeling', 'product development', 'fmea', 'quality control',
        'circuit design', 'electrical systems', 'electronics', 'power systems', 'control systems',
        'programming', 'renewable energy', 'automation', 'embedded systems'
    ],
    
    # Hospitality & Tourism Skills
    'hospitality': [
        'hospitality management', 'customer service', 'staff supervision', 'operations',
        'guest relations', 'revenue management', 'event planning', 'food service', 'marketing',
        'cooking techniques', 'food safety', 'menu planning', 'kitchen management', 'culinary arts',
        'wine pairing', 'international cuisine', 'cost control', 'food presentation',
        'travel planning', 'booking systems', 'destination knowledge', 'itinerary planning',
        'specialized travel', 'group bookings', 'crisis management', 'sales'
    ],
    
    # Government & Public Sector Skills
    'government': [
        'policy research', 'data analysis', 'report writing', 'government processes',
        'stakeholder engagement', 'statistics', 'economic analysis', 'legislative process',
        'public administration', 'program management', 'budget administration', 'public policy',
        'leadership', 'strategic planning', 'performance measurement', 'stakeholder relations',
        'change management', 'crisis management'
    ],
    
    # Non-Profit Skills
    'nonprofit': [
        'program management', 'fundraising', 'grant writing', 'volunteer coordination',
        'community outreach', 'donor relations', 'event planning', 'advocacy', 'strategic planning',
        'case management', 'counseling', 'social services', 'client advocacy', 'crisis intervention',
        'group therapy', 'community organizing', 'policy advocacy', 'trauma informed care'
    ],
    
    # Manufacturing Skills
    'manufacturing': [
        'production planning', 'quality control', 'inventory management', 'safety',
        'lean manufacturing', 'six sigma', 'automation', 'supply chain', 'continuous improvement',
        'statistical analysis', 'process improvement', 'inspection', 'iso standards',
        'root cause analysis', 'auditing', 'quality management systems'
    ],
    
    # Retail Skills
    'retail': [
        'retail management', 'customer service', 'staff supervision', 'inventory control',
        'sales analysis', 'visual merchandising', 'loss prevention', 'budget management',
        'team leadership', 'purchasing', 'vendor management', 'negotiation', 'inventory planning',
        'market analysis', 'trend forecasting', 'supply chain', 'category management', 'cost analysis'
    ],
    
    # Business & Management Skills
    'business': [
        'business analysis', 'requirements gathering', 'process improvement', 'project management',
        'leadership', 'communication', 'risk management', 'budget management', 'agile', 'scrum',
        'stakeholder management', 'quality assurance', 'recruitment', 'employee relations',
        'hr policies', 'performance management', 'compliance', 'hr analytics', 'talent management',
        'organizational development', 'benefits administration'
    ],
    
    # Soft Skills (Universal across sectors)
    'soft_skills': [
        'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
        'time management', 'organization', 'adaptability', 'creativity', 'emotional intelligence',
        'conflict resolution', 'mentoring', 'coaching', 'presentation skills', 'interpersonal skills',
        'customer service', 'sales', 'negotiation', 'project management', 'strategic thinking'
    ]
}

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_skills(text: str) -> Dict[str, List[str]]:
    """Extract skills from text using precise keyword matching"""
    text_lower = text.lower()
    extracted_skills = {}
    
    for category, skills in SKILL_KEYWORDS.items():
        found_skills = []
        for skill in skills:
            skill_lower = skill.lower()
            
            # For single-word skills, use word boundary matching
            if ' ' not in skill_lower:
                # Use word boundary pattern to avoid false positives
                pattern = r'\b' + re.escape(skill_lower) + r'\b'
                if re.search(pattern, text_lower):
                    # Additional check for single-letter skills to avoid false positives
                    if len(skill_lower) == 1:
                        # For single letters like 'r', check if it's in a programming context
                        if skill_lower == 'r':
                            # Look for R in programming language contexts
                            programming_contexts = [
                                r'\bprogramming\s+languages?\b',
                                r'\blanguages?\b',
                                r'\btechnologies?\b',
                                r'\bskills?\b',
                                r'\btech\s+stack\b',
                                r'\bprogramming\b',
                                r'\bcoding\b',
                                r'\bdevelopment\b'
                            ]
                            # Check if R appears near programming-related words
                            found_in_context = False
                            for context_pattern in programming_contexts:
                                if re.search(context_pattern, text_lower):
                                    # Look for R within 50 characters of programming context
                                    context_matches = re.finditer(context_pattern, text_lower)
                                    for match in context_matches:
                                        start = max(0, match.start() - 50)
                                        end = min(len(text_lower), match.end() + 50)
                                        context_text = text_lower[start:end]
                                        if re.search(r'\br\b', context_text):
                                            found_in_context = True
                                            break
                                    if found_in_context:
                                        break
                            
                            if found_in_context:
                                found_skills.append(skill)
                        else:
                            # For other single-letter skills, just check word boundary
                            found_skills.append(skill)
                    else:
                        # For multi-letter single words, use word boundary
                        found_skills.append(skill)
            else:
                # For multi-word skills, use phrase matching
                pattern = r'\b' + re.escape(skill_lower) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append(skill)
        
        if found_skills:
            extracted_skills[category] = found_skills
    
    return extracted_skills

def extract_name(text: str) -> Optional[str]:
    """Extract person name from text using improved pattern matching"""
    lines = text.split('\n')
    
    # Look for name in the first few lines (typical resume format)
    for i, line in enumerate(lines[:5]):
        line = line.strip()
        if not line:
            continue
            
        # Skip lines that are clearly not names
        if any(char.isdigit() for char in line):  # Contains numbers
            continue
        if '@' in line:  # Contains email
            continue
        if '|' in line or '•' in line:  # Contains separators
            continue
        if len(line) < 3 or len(line) > 50:  # Too short or too long
            continue
            
        # Check if line looks like a name (2-4 words, reasonable length)
        words = line.split()
        if 2 <= len(words) <= 4:
            # Check if all words are reasonable for names
            if all(len(word) >= 2 for word in words):
                # This looks like a name - return it
                return line
    
    # Fallback to spaCy NER but with better filtering
    doc = nlp(text)
    names = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            name = ent.text.strip()
            # Filter out names that are too short or too long
            if 3 <= len(name) <= 50:
                # Filter out names that contain numbers or special characters
                if not any(char.isdigit() for char in name) and '@' not in name:
                    names.append(name)
    
    return names[0] if names else None

def extract_email(text: str) -> Optional[str]:
    """Extract email address from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text"""
    phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
    phones = re.findall(phone_pattern, text)
    if phones:
        return ''.join(phones[0])
    return None

def extract_education(text: str) -> List[str]:
    """Extract education information"""
    education_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'degree', 'university', 'college']
    lines = text.split('\n')
    education_lines = []
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in education_keywords):
            education_lines.append(line.strip())
    
    return education_lines

def extract_experience(text: str) -> List[str]:
    """Extract work experience information with job titles"""
    lines = text.split('\n')
    experience_lines = []
    
    # Look for experience section and extract job titles
    in_experience_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Check if we're entering experience section
        if any(keyword in line_lower for keyword in ['work experience', 'experience', 'employment history', 'professional experience']):
            in_experience_section = True
            continue
        
        # If we're in experience section, look for job titles
        if in_experience_section and line.strip():
            # Look for patterns like "Job Title | Company | Date" or "Job Title at Company"
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 2:
                    job_title = parts[0].strip()
                    if job_title and len(job_title.split()) <= 4:  # Reasonable job title length
                        experience_lines.append(line.strip())
            elif ' at ' in line_lower or ' - ' in line or ' | ' in line:
                # Extract job title from various formats
                if ' at ' in line_lower:
                    parts = line.split(' at ')
                    if len(parts) >= 2:
                        job_title = parts[0].strip()
                        if job_title and len(job_title.split()) <= 4:
                            experience_lines.append(line.strip())
                elif ' - ' in line:
                    parts = line.split(' - ')
                    if len(parts) >= 2:
                        job_title = parts[0].strip()
                        if job_title and len(job_title.split()) <= 4:
                            experience_lines.append(line.strip())
                elif ' | ' in line:
                    parts = line.split(' | ')
                    if len(parts) >= 2:
                        job_title = parts[0].strip()
                        if job_title and len(job_title.split()) <= 4:
                            experience_lines.append(line.strip())
            
            # Also capture lines that look like job descriptions (bullet points)
            elif line.strip().startswith('•') or line.strip().startswith('-'):
                experience_lines.append(line.strip())
    
    # If no structured experience found, look for any lines that might be job titles
    if not experience_lines:
        for line in lines:
            line_lower = line.lower().strip()
            # Look for common job title patterns
            if any(title in line_lower for title in ['engineer', 'developer', 'manager', 'analyst', 'specialist', 'coordinator', 'director']):
                if '|' in line or ' at ' in line_lower or ' - ' in line:
                    experience_lines.append(line.strip())
    
    return experience_lines

def parse_resume(file_path: str) -> Dict:
    """Main function to parse resume and extract all information"""
    # Determine file type and extract text
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
    # Extract information
    parsed_data = {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text),
        'education': extract_education(text),
        'experience': extract_experience(text),
        'raw_text': text[:1000] + "..." if len(text) > 1000 else text  # Limit raw text length
    }
    
    return parsed_data

def parse_resume_text(text: str) -> Dict:
    """Parse resume from text string"""
    parsed_data = {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text),
        'education': extract_education(text),
        'experience': extract_experience(text),
        'raw_text': text[:1000] + "..." if len(text) > 1000 else text
    }
    
    return parsed_data 