import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Tuple
import joblib
import os

# Comprehensive job profiles across all sectors
JOB_PROFILES = {
    # Technology & IT Sector
    'software_engineer': {
        'title': 'Software Engineer',
        'description': 'Design, develop, and maintain software applications',
        'required_skills': ['programming', 'algorithms', 'git', 'databases', 'web_development'],
        'sector': 'technology'
    },
    'data_scientist': {
        'title': 'Data Scientist',
        'description': 'Analyze complex data to help organizations make better decisions',
        'required_skills': ['python', 'statistics', 'machine learning', 'data visualization', 'sql'],
        'sector': 'technology'
    },
    'machine_learning_engineer': {
        'title': 'Machine Learning Engineer',
        'description': 'Design and deploy machine learning models at scale',
        'required_skills': ['python', 'machine learning', 'deep learning', 'git', 'cloud_platforms'],
        'sector': 'technology'
    },
    'web_developer': {
        'title': 'Web Developer',
        'description': 'Build and maintain websites and web applications',
        'required_skills': ['html', 'css', 'javascript', 'web_development', 'databases'],
        'sector': 'technology'
    },
    'devops_engineer': {
        'title': 'DevOps Engineer',
        'description': 'Automate and optimize software deployment and infrastructure',
        'required_skills': ['docker', 'kubernetes', 'ci/cd', 'cloud_platforms', 'git'],
        'sector': 'technology'
    },
    
    # Healthcare Sector
    'registered_nurse': {
        'title': 'Registered Nurse',
        'description': 'Provide patient care and support in healthcare settings',
        'required_skills': ['patient care', 'medical terminology', 'clinical skills', 'cpr', 'medication administration'],
        'sector': 'healthcare'
    },
    'physician': {
        'title': 'Physician',
        'description': 'Diagnose and treat patients in medical practice',
        'required_skills': ['medical diagnosis', 'anatomy', 'patient care', 'clinical skills', 'medical terminology'],
        'sector': 'healthcare'
    },
    'pharmacist': {
        'title': 'Pharmacist',
        'description': 'Dispense medications and provide pharmaceutical care',
        'required_skills': ['pharmacy', 'drug interactions', 'prescription', 'medication administration', 'patient care'],
        'sector': 'healthcare'
    },
    'physical_therapist': {
        'title': 'Physical Therapist',
        'description': 'Help patients recover movement and manage pain',
        'required_skills': ['physical therapy', 'rehabilitation', 'patient assessment', 'treatment planning', 'anatomy'],
        'sector': 'healthcare'
    },
    'healthcare_administrator': {
        'title': 'Healthcare Administrator',
        'description': 'Manage healthcare facilities and operations',
        'required_skills': ['leadership', 'healthcare', 'management', 'budget management', 'communication'],
        'sector': 'healthcare'
    },
    
    # Finance Sector
    'financial_analyst': {
        'title': 'Financial Analyst',
        'description': 'Analyze financial data and provide investment guidance',
        'required_skills': ['financial analysis', 'excel', 'financial modeling', 'accounting', 'budgeting'],
        'sector': 'finance'
    },
    'accountant': {
        'title': 'Accountant',
        'description': 'Manage financial records and ensure compliance',
        'required_skills': ['accounting', 'bookkeeping', 'tax preparation', 'financial reporting', 'excel'],
        'sector': 'finance'
    },
    'investment_banker': {
        'title': 'Investment Banker',
        'description': 'Help companies raise capital and execute financial transactions',
        'required_skills': ['financial analysis', 'investment analysis', 'valuation', 'corporate finance', 'excel'],
        'sector': 'finance'
    },
    'risk_analyst': {
        'title': 'Risk Analyst',
        'description': 'Assess and manage financial and operational risks',
        'required_skills': ['risk management', 'financial analysis', 'statistics', 'excel', 'regulatory compliance'],
        'sector': 'finance'
    },
    'financial_advisor': {
        'title': 'Financial Advisor',
        'description': 'Provide financial planning and investment advice to clients',
        'required_skills': ['financial analysis', 'investment analysis', 'communication', 'sales', 'customer service'],
        'sector': 'finance'
    },
    
    # Education Sector
    'teacher': {
        'title': 'Teacher',
        'description': 'Educate students in various subjects and grade levels',
        'required_skills': ['teaching', 'curriculum development', 'classroom management', 'communication', 'lesson planning'],
        'sector': 'education'
    },
    'professor': {
        'title': 'Professor',
        'description': 'Teach and conduct research at university level',
        'required_skills': ['teaching', 'research', 'academic writing', 'subject expertise', 'publication'],
        'sector': 'education'
    },
    'school_administrator': {
        'title': 'School Administrator',
        'description': 'Manage educational institutions and staff',
        'required_skills': ['leadership', 'education', 'management', 'budget management', 'communication'],
        'sector': 'education'
    },
    'special_education_teacher': {
        'title': 'Special Education Teacher',
        'description': 'Work with students who have special needs',
        'required_skills': ['special education', 'teaching', 'patience', 'communication', 'lesson planning'],
        'sector': 'education'
    },
    'guidance_counselor': {
        'title': 'Guidance Counselor',
        'description': 'Provide academic and career guidance to students',
        'required_skills': ['counseling', 'communication', 'career guidance', 'academic advising', 'mentoring'],
        'sector': 'education'
    },
    
    # Marketing & Sales Sector
    'marketing_manager': {
        'title': 'Marketing Manager',
        'description': 'Develop and execute marketing strategies for organizations',
        'required_skills': ['marketing strategy', 'digital marketing', 'analytics', 'project management', 'brand management'],
        'sector': 'marketing'
    },
    'sales_representative': {
        'title': 'Sales Representative',
        'description': 'Sell products or services to customers',
        'required_skills': ['sales techniques', 'customer relationship management', 'negotiation', 'product knowledge', 'communication'],
        'sector': 'marketing'
    },
    'digital_marketing_specialist': {
        'title': 'Digital Marketing Specialist',
        'description': 'Create and manage online marketing campaigns',
        'required_skills': ['digital marketing', 'social media', 'seo', 'content creation', 'analytics'],
        'sector': 'marketing'
    },
    'market_researcher': {
        'title': 'Market Researcher',
        'description': 'Conduct research to understand market trends and consumer behavior',
        'required_skills': ['market research', 'data analysis', 'statistics', 'communication', 'report writing'],
        'sector': 'marketing'
    },
    'brand_manager': {
        'title': 'Brand Manager',
        'description': 'Develop and maintain brand identity and strategy',
        'required_skills': ['brand management', 'marketing strategy', 'communication', 'project management', 'analytics'],
        'sector': 'marketing'
    },
    
    # Legal Sector
    'attorney': {
        'title': 'Attorney',
        'description': 'Provide legal representation and counsel to clients',
        'required_skills': ['legal research', 'contract law', 'litigation', 'legal writing', 'client counseling'],
        'sector': 'legal'
    },
    'paralegal': {
        'title': 'Paralegal',
        'description': 'Support attorneys with legal research and document preparation',
        'required_skills': ['legal research', 'document preparation', 'legal terminology', 'organization', 'communication'],
        'sector': 'legal'
    },
    'legal_assistant': {
        'title': 'Legal Assistant',
        'description': 'Provide administrative support to legal professionals',
        'required_skills': ['organization', 'communication', 'document preparation', 'legal terminology', 'case management'],
        'sector': 'legal'
    },
    'compliance_officer': {
        'title': 'Compliance Officer',
        'description': 'Ensure organizations follow laws and regulations',
        'required_skills': ['regulatory compliance', 'legal research', 'risk management', 'communication', 'audit'],
        'sector': 'legal'
    },
    'mediator': {
        'title': 'Mediator',
        'description': 'Facilitate conflict resolution between parties',
        'required_skills': ['mediation', 'communication', 'negotiation', 'conflict resolution', 'patience'],
        'sector': 'legal'
    },
    
    # Engineering Sector
    'civil_engineer': {
        'title': 'Civil Engineer',
        'description': 'Design and oversee construction of infrastructure projects',
        'required_skills': ['autocad', 'structural analysis', 'project management', 'engineering design', 'construction'],
        'sector': 'engineering'
    },
    'mechanical_engineer': {
        'title': 'Mechanical Engineer',
        'description': 'Design and develop mechanical systems and products',
        'required_skills': ['solidworks', 'mechanical design', 'thermodynamics', 'materials science', 'manufacturing'],
        'sector': 'engineering'
    },
    'electrical_engineer': {
        'title': 'Electrical Engineer',
        'description': 'Design electrical systems and electronic devices',
        'required_skills': ['circuit design', 'electrical systems', 'electronics', 'power systems', 'control systems'],
        'sector': 'engineering'
    },
    'chemical_engineer': {
        'title': 'Chemical Engineer',
        'description': 'Design processes for chemical manufacturing and production',
        'required_skills': ['chemical processes', 'thermodynamics', 'materials science', 'safety', 'manufacturing'],
        'sector': 'engineering'
    },
    'software_engineer_embedded': {
        'title': 'Embedded Systems Engineer',
        'description': 'Develop software for embedded systems and IoT devices',
        'required_skills': ['programming', 'embedded systems', 'electronics', 'real-time systems', 'hardware'],
        'sector': 'engineering'
    },
    
    # Hospitality & Tourism Sector
    'hotel_manager': {
        'title': 'Hotel Manager',
        'description': 'Manage hotel operations and guest services',
        'required_skills': ['hospitality management', 'customer service', 'staff supervision', 'operations', 'guest relations'],
        'sector': 'hospitality'
    },
    'chef': {
        'title': 'Chef',
        'description': 'Create and oversee food preparation in restaurants',
        'required_skills': ['cooking techniques', 'food safety', 'menu planning', 'kitchen management', 'culinary arts'],
        'sector': 'hospitality'
    },
    'travel_agent': {
        'title': 'Travel Agent',
        'description': 'Plan and book travel arrangements for clients',
        'required_skills': ['travel planning', 'booking systems', 'destination knowledge', 'customer service', 'sales'],
        'sector': 'hospitality'
    },
    'event_planner': {
        'title': 'Event Planner',
        'description': 'Coordinate and manage events and conferences',
        'required_skills': ['event planning', 'project management', 'vendor management', 'communication', 'organization'],
        'sector': 'hospitality'
    },
    'restaurant_manager': {
        'title': 'Restaurant Manager',
        'description': 'Oversee restaurant operations and staff',
        'required_skills': ['food service', 'staff supervision', 'customer service', 'operations', 'cost control'],
        'sector': 'hospitality'
    },
    
    # Government & Public Sector
    'policy_analyst': {
        'title': 'Policy Analyst',
        'description': 'Research and analyze government policies and programs',
        'required_skills': ['policy research', 'data analysis', 'report writing', 'government processes', 'stakeholder engagement'],
        'sector': 'government'
    },
    'public_administrator': {
        'title': 'Public Administrator',
        'description': 'Manage government programs and public services',
        'required_skills': ['public administration', 'program management', 'budget administration', 'leadership', 'communication'],
        'sector': 'government'
    },
    'urban_planner': {
        'title': 'Urban Planner',
        'description': 'Plan and develop communities and infrastructure',
        'required_skills': ['urban planning', 'gis', 'project management', 'community engagement', 'sustainability'],
        'sector': 'government'
    },
    'social_worker': {
        'title': 'Social Worker',
        'description': 'Help people solve and cope with problems in their lives',
        'required_skills': ['case management', 'counseling', 'social services', 'client advocacy', 'crisis intervention'],
        'sector': 'government'
    },
    'environmental_specialist': {
        'title': 'Environmental Specialist',
        'description': 'Monitor and protect environmental resources',
        'required_skills': ['environmental science', 'regulatory compliance', 'data analysis', 'report writing', 'sustainability'],
        'sector': 'government'
    },
    
    # Non-Profit Sector
    'nonprofit_manager': {
        'title': 'Nonprofit Manager',
        'description': 'Manage nonprofit organizations and programs',
        'required_skills': ['program management', 'fundraising', 'grant writing', 'volunteer coordination', 'community outreach'],
        'sector': 'nonprofit'
    },
    'fundraiser': {
        'title': 'Fundraiser',
        'description': 'Raise funds for nonprofit organizations',
        'required_skills': ['fundraising', 'donor relations', 'communication', 'sales', 'event planning'],
        'sector': 'nonprofit'
    },
    'advocacy_specialist': {
        'title': 'Advocacy Specialist',
        'description': 'Advocate for social causes and policy change',
        'required_skills': ['advocacy', 'policy advocacy', 'communication', 'community organizing', 'campaign management'],
        'sector': 'nonprofit'
    },
    'volunteer_coordinator': {
        'title': 'Volunteer Coordinator',
        'description': 'Recruit and manage volunteers for organizations',
        'required_skills': ['volunteer coordination', 'recruitment', 'training', 'communication', 'organization'],
        'sector': 'nonprofit'
    },
    'program_director': {
        'title': 'Program Director',
        'description': 'Oversee program development and implementation',
        'required_skills': ['program management', 'strategic planning', 'leadership', 'budget management', 'evaluation'],
        'sector': 'nonprofit'
    },
    
    # Manufacturing Sector
    'production_manager': {
        'title': 'Production Manager',
        'description': 'Oversee manufacturing operations and production processes',
        'required_skills': ['production planning', 'quality control', 'inventory management', 'safety', 'lean manufacturing'],
        'sector': 'manufacturing'
    },
    'quality_control_specialist': {
        'title': 'Quality Control Specialist',
        'description': 'Ensure products meet quality standards and specifications',
        'required_skills': ['quality control', 'inspection', 'iso standards', 'statistical analysis', 'process improvement'],
        'sector': 'manufacturing'
    },
    'industrial_engineer': {
        'title': 'Industrial Engineer',
        'description': 'Optimize production processes and systems',
        'required_skills': ['process improvement', 'lean manufacturing', 'six sigma', 'statistical analysis', 'automation'],
        'sector': 'manufacturing'
    },
    'maintenance_technician': {
        'title': 'Maintenance Technician',
        'description': 'Maintain and repair manufacturing equipment',
        'required_skills': ['equipment maintenance', 'troubleshooting', 'safety', 'technical skills', 'preventive maintenance'],
        'sector': 'manufacturing'
    },
    'supply_chain_analyst': {
        'title': 'Supply Chain Analyst',
        'description': 'Analyze and optimize supply chain operations',
        'required_skills': ['supply chain', 'inventory management', 'data analysis', 'logistics', 'cost analysis'],
        'sector': 'manufacturing'
    },
    
    # Retail Sector
    'retail_manager': {
        'title': 'Retail Manager',
        'description': 'Manage retail store operations and staff',
        'required_skills': ['retail management', 'customer service', 'staff supervision', 'inventory control', 'sales analysis'],
        'sector': 'retail'
    },
    'merchandiser': {
        'title': 'Merchandiser',
        'description': 'Plan and manage product displays and inventory',
        'required_skills': ['visual merchandising', 'inventory planning', 'trend forecasting', 'category management', 'sales analysis'],
        'sector': 'retail'
    },
    'buyer': {
        'title': 'Buyer',
        'description': 'Purchase products for retail organizations',
        'required_skills': ['purchasing', 'vendor management', 'negotiation', 'market analysis', 'inventory planning'],
        'sector': 'retail'
    },
    'loss_prevention_specialist': {
        'title': 'Loss Prevention Specialist',
        'description': 'Prevent theft and reduce losses in retail environments',
        'required_skills': ['loss prevention', 'security', 'investigation', 'customer service', 'surveillance'],
        'sector': 'retail'
    },
    'ecommerce_specialist': {
        'title': 'E-commerce Specialist',
        'description': 'Manage online retail operations and digital sales',
        'required_skills': ['ecommerce', 'digital marketing', 'online sales', 'customer service', 'analytics'],
        'sector': 'retail'
    },
    
    # Business & Management Sector
    'business_analyst': {
        'title': 'Business Analyst',
        'description': 'Analyze business processes and recommend improvements',
        'required_skills': ['business analysis', 'requirements gathering', 'process improvement', 'project management', 'communication'],
        'sector': 'business'
    },
    'project_manager': {
        'title': 'Project Manager',
        'description': 'Plan and execute projects to achieve organizational goals',
        'required_skills': ['project management', 'leadership', 'communication', 'risk management', 'budget management'],
        'sector': 'business'
    },
    'human_resources_manager': {
        'title': 'Human Resources Manager',
        'description': 'Manage employee relations and HR policies',
        'required_skills': ['recruitment', 'employee relations', 'hr policies', 'performance management', 'communication'],
        'sector': 'business'
    },
    'operations_manager': {
        'title': 'Operations Manager',
        'description': 'Oversee daily operations and improve efficiency',
        'required_skills': ['operations management', 'process improvement', 'leadership', 'budget management', 'quality control'],
        'sector': 'business'
    },
    'consultant': {
        'title': 'Management Consultant',
        'description': 'Provide strategic advice to improve business performance',
        'required_skills': ['strategic planning', 'business analysis', 'communication', 'problem solving', 'project management'],
        'sector': 'business'
    }
}

# Learning resources mapping for all sectors
LEARNING_RESOURCES = {
    # Technology Skills
    'python': {
        'courses': [
            'https://www.coursera.org/learn/python',
            'https://www.udemy.com/course/complete-python-bootcamp/',
            'https://www.freecodecamp.org/learn/scientific-computing-with-python/'
        ],
        'books': ['Python Crash Course', 'Automate the Boring Stuff with Python'],
        'practice': ['HackerRank', 'LeetCode', 'Codewars']
    },
    'machine learning': {
        'courses': [
            'https://www.coursera.org/learn/machine-learning',
            'https://www.udemy.com/course/machinelearning/',
            'https://www.fast.ai/'
        ],
        'books': ['Hands-On Machine Learning', 'Introduction to Statistical Learning'],
        'practice': ['Kaggle', 'Google Colab', 'Paperspace']
    },
    'sql': {
        'courses': [
            'https://www.coursera.org/learn/sql-for-data-science',
            'https://www.udemy.com/course/the-complete-sql-bootcamp/',
            'https://www.freecodecamp.org/learn/relational-database/'
        ],
        'books': ['SQL for Data Analysis', 'Learning SQL'],
        'practice': ['HackerRank SQL', 'LeetCode Database', 'SQLZoo']
    },
    'javascript': {
        'courses': [
            'https://www.udemy.com/course/the-complete-javascript-course/',
            'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/',
            'https://javascript.info/'
        ],
        'books': ['Eloquent JavaScript', 'You Don\'t Know JS'],
        'practice': ['Codewars', 'HackerRank', 'Frontend Mentor']
    },
    'react': {
        'courses': [
            'https://www.udemy.com/course/react-the-complete-guide-incl-redux/',
            'https://www.freecodecamp.org/learn/front-end-development-libraries/',
            'https://react.dev/learn'
        ],
        'books': ['Learning React', 'React Design Patterns'],
        'practice': ['Frontend Mentor', 'React Challenges', 'Build projects']
    },
    'docker': {
        'courses': [
            'https://www.udemy.com/course/docker-mastery/',
            'https://www.coursera.org/learn/docker-container',
            'https://docs.docker.com/get-started/'
        ],
        'books': ['Docker in Action', 'The Docker Book'],
        'practice': ['Docker Hub', 'Build containerized apps', 'Docker playground']
    },
    'aws': {
        'courses': [
            'https://www.udemy.com/course/aws-certified-solutions-architect-associate/',
            'https://www.coursera.org/learn/aws-cloud-technical-essentials',
            'https://aws.amazon.com/training/'
        ],
        'books': ['AWS Certified Solutions Architect Study Guide', 'AWS in Action'],
        'practice': ['AWS Free Tier', 'AWS CloudFormation', 'Build projects on AWS']
    },
    
    # Healthcare Skills
    'patient care': {
        'courses': [
            'https://www.coursera.org/learn/patient-care',
            'https://www.edx.org/learn/nursing',
            'https://www.udemy.com/course/patient-care-technician/'
        ],
        'books': ['Fundamentals of Nursing', 'Patient Care Skills'],
        'practice': ['Clinical Simulations', 'Hospital Volunteering', 'Nursing Labs']
    },
    'medical terminology': {
        'courses': [
            'https://www.coursera.org/learn/medical-terminology',
            'https://www.khanacademy.org/science/health-and-medicine',
            'https://www.edx.org/learn/anatomy-physiology'
        ],
        'books': ['Medical Terminology for Health Professions', 'The Language of Medicine'],
        'practice': ['Medical Dictionary Apps', 'Flashcards', 'Online Quizzes']
    },
    'cpr': {
        'courses': [
            'https://www.heart.org/en/cpr',
            'https://www.redcross.org/take-a-class/cpr',
            'https://www.aha.org/cpr'
        ],
        'books': ['CPR Guidelines', 'Emergency Care'],
        'practice': ['CPR Training Centers', 'Simulation Labs', 'Practice Mannequins']
    },
    
    # Finance Skills
    'financial analysis': {
        'courses': [
            'https://www.coursera.org/learn/financial-analysis',
            'https://www.edx.org/learn/corporate-finance',
            'https://www.udemy.com/course/financial-analysis/'
        ],
        'books': ['Financial Statement Analysis', 'Valuation: Measuring and Managing the Value of Companies'],
        'practice': ['Bloomberg Terminal', 'Yahoo Finance', 'Financial Modeling']
    },
    'excel': {
        'courses': [
            'https://www.coursera.org/learn/excel-skills-for-business',
            'https://www.udemy.com/course/microsoft-excel-2013-from-beginner-to-advanced-and-beyond/',
            'https://www.edx.org/learn/microsoft-excel'
        ],
        'books': ['Excel 2019 Bible', 'Advanced Excel Formulas'],
        'practice': ['Excel Practice Files', 'Financial Modeling', 'Data Analysis Projects']
    },
    'accounting': {
        'courses': [
            'https://www.coursera.org/learn/financial-accounting',
            'https://www.edx.org/learn/accounting',
            'https://www.udemy.com/course/accounting-basics/'
        ],
        'books': ['Financial Accounting', 'Intermediate Accounting'],
        'practice': ['QuickBooks Practice', 'Accounting Software', 'Case Studies']
    },
    
    # Education Skills
    'teaching': {
        'courses': [
            'https://www.coursera.org/learn/foundations-of-teaching',
            'https://www.edx.org/learn/teaching',
            'https://www.udemy.com/course/teaching-skills/'
        ],
        'books': ['The First Days of School', 'Teach Like a Champion'],
        'practice': ['Student Teaching', 'Tutoring', 'Classroom Observations']
    },
    'curriculum development': {
        'courses': [
            'https://www.coursera.org/learn/curriculum-design',
            'https://www.edx.org/learn/instructional-design',
            'https://www.udemy.com/course/curriculum-development/'
        ],
        'books': ['Understanding by Design', 'Curriculum Development'],
        'practice': ['Lesson Planning', 'Curriculum Mapping', 'Educational Projects']
    },
    'classroom management': {
        'courses': [
            'https://www.coursera.org/learn/classroom-management',
            'https://www.edx.org/learn/positive-behavior-support',
            'https://www.udemy.com/course/classroom-management/'
        ],
        'books': ['The Classroom Management Book', 'Discipline with Dignity'],
        'practice': ['Student Teaching', 'Classroom Observations', 'Behavior Management']
    },
    
    # Marketing Skills
    'digital marketing': {
        'courses': [
            'https://www.coursera.org/learn/digital-marketing',
            'https://learndigital.withgoogle.com/digitalgarage/',
            'https://academy.hubspot.com/'
        ],
        'books': ['Digital Marketing for Dummies', 'Contagious: Why Things Catch On'],
        'practice': ['Google Ads', 'Facebook Ads', 'Social Media Management']
    },
    'social media': {
        'courses': [
            'https://www.coursera.org/learn/social-media-marketing',
            'https://www.udemy.com/course/social-media-marketing-strategy/',
            'https://www.edx.org/learn/social-media'
        ],
        'books': ['Jab, Jab, Jab, Right Hook', 'The Art of Social Media'],
        'practice': ['Personal Branding', 'Content Creation', 'Social Media Analytics']
    },
    'seo': {
        'courses': [
            'https://www.coursera.org/learn/seo-fundamentals',
            'https://www.udemy.com/course/technical-seo/',
            'https://www.google.com/analytics/academy/'
        ],
        'books': ['SEO for Dummies', 'The Art of SEO'],
        'practice': ['Website Optimization', 'Keyword Research', 'SEO Tools']
    },
    
    # Legal Skills
    'legal research': {
        'courses': [
            'https://www.coursera.org/learn/legal-research',
            'https://www.edx.org/learn/legal-writing',
            'https://www.udemy.com/course/legal-research/'
        ],
        'books': ['Legal Research in a Nutshell', 'Introduction to Legal Research'],
        'practice': ['Westlaw', 'LexisNexis', 'Legal Databases']
    },
    'contract law': {
        'courses': [
            'https://www.coursera.org/learn/contract-law',
            'https://www.edx.org/learn/business-law',
            'https://www.udemy.com/course/contract-law/'
        ],
        'books': ['Contracts: Examples and Explanations', 'Contract Law for Dummies'],
        'practice': ['Contract Drafting', 'Case Studies', 'Legal Writing']
    },
    'litigation': {
        'courses': [
            'https://www.coursera.org/learn/civil-litigation',
            'https://www.edx.org/learn/trial-advocacy',
            'https://www.udemy.com/course/litigation/'
        ],
        'books': ['Civil Procedure', 'Trial Techniques'],
        'practice': ['Moot Court', 'Mock Trials', 'Legal Clinics']
    },
    
    # Engineering Skills
    'autocad': {
        'courses': [
            'https://www.udemy.com/course/autocad-2018-course/',
            'https://www.autodesk.com/certification',
            'https://www.edx.org/learn/autocad'
        ],
        'books': ['AutoCAD 2022 Tutorial', 'Mastering AutoCAD'],
        'practice': ['AutoCAD Software', 'Design Projects', 'Portfolio Building']
    },
    'solidworks': {
        'courses': [
            'https://www.udemy.com/course/solidworks-course/',
            'https://www.dassault-systemes.com/certification',
            'https://www.edx.org/learn/solidworks'
        ],
        'books': ['SolidWorks 2022 Tutorial', 'Mastering SolidWorks'],
        'practice': ['SolidWorks Software', '3D Modeling Projects', 'Design Portfolio']
    },
    'structural analysis': {
        'courses': [
            'https://www.coursera.org/learn/structural-analysis',
            'https://www.edx.org/learn/engineering-mechanics',
            'https://www.udemy.com/course/structural-analysis/'
        ],
        'books': ['Structural Analysis', 'Mechanics of Materials'],
        'practice': ['Engineering Software', 'Design Projects', 'Structural Modeling']
    },
    
    # Hospitality Skills
    'hospitality management': {
        'courses': [
            'https://www.coursera.org/learn/hospitality-management',
            'https://www.edx.org/learn/hotel-operations',
            'https://www.udemy.com/course/hospitality-management/'
        ],
        'books': ['Hospitality Management', 'Hotel Operations Management'],
        'practice': ['Hotel Internships', 'Restaurant Management', 'Event Planning']
    },
    'customer service': {
        'courses': [
            'https://www.coursera.org/learn/customer-service',
            'https://www.udemy.com/course/customer-experience/',
            'https://www.edx.org/learn/customer-service'
        ],
        'books': ['The Customer Service Revolution', 'Delivering Happiness'],
        'practice': ['Customer Service Roles', 'Role-playing', 'Service Excellence']
    },
    'cooking techniques': {
        'courses': [
            'https://www.coursera.org/learn/culinary-arts',
            'https://www.udemy.com/course/cooking-fundamentals/',
            'https://www.edx.org/learn/cooking'
        ],
        'books': ['The Professional Chef', 'On Food and Cooking'],
        'practice': ['Cooking Classes', 'Kitchen Internships', 'Recipe Development']
    },
    
    # Government Skills
    'policy research': {
        'courses': [
            'https://www.coursera.org/learn/public-policy',
            'https://www.edx.org/learn/policy-analysis',
            'https://www.udemy.com/course/policy-research/'
        ],
        'books': ['Policy Analysis', 'Public Policy Making'],
        'practice': ['Policy Research', 'Government Internships', 'Policy Writing']
    },
    'public administration': {
        'courses': [
            'https://www.coursera.org/learn/public-administration',
            'https://www.edx.org/learn/government-management',
            'https://www.udemy.com/course/public-administration/'
        ],
        'books': ['Public Administration', 'The New Public Service'],
        'practice': ['Government Internships', 'Public Service', 'Administrative Projects']
    },
    'stakeholder engagement': {
        'courses': [
            'https://www.coursera.org/learn/stakeholder-management',
            'https://www.edx.org/learn/public-engagement',
            'https://www.udemy.com/course/stakeholder-engagement/'
        ],
        'books': ['Stakeholder Theory', 'Engaging Stakeholders'],
        'practice': ['Community Outreach', 'Public Meetings', 'Stakeholder Interviews']
    },
    
    # Non-Profit Skills
    'fundraising': {
        'courses': [
            'https://www.coursera.org/learn/fundraising',
            'https://www.edx.org/learn/nonprofit-management',
            'https://www.udemy.com/course/fundraising/'
        ],
        'books': ['Fundraising for Dummies', 'The Fundraising Plan'],
        'practice': ['Fundraising Events', 'Donor Relations', 'Grant Writing']
    },
    'grant writing': {
        'courses': [
            'https://www.coursera.org/learn/grant-writing',
            'https://www.edx.org/learn/proposal-writing',
            'https://www.udemy.com/course/grant-writing/'
        ],
        'books': ['Grant Writing for Dummies', 'The Only Grant Writing Book You\'ll Ever Need'],
        'practice': ['Grant Applications', 'Proposal Writing', 'Foundation Research']
    },
    'volunteer coordination': {
        'courses': [
            'https://www.coursera.org/learn/volunteer-management',
            'https://www.edx.org/learn/nonprofit-leadership',
            'https://www.udemy.com/course/volunteer-coordination/'
        ],
        'books': ['Volunteer Management', 'The Volunteer Management Handbook'],
        'practice': ['Volunteer Coordination', 'Event Planning', 'Community Outreach']
    },
    
    # Manufacturing Skills
    'lean manufacturing': {
        'courses': [
            'https://www.coursera.org/learn/lean-manufacturing',
            'https://www.edx.org/learn/six-sigma',
            'https://www.udemy.com/course/lean-manufacturing/'
        ],
        'books': ['The Toyota Way', 'Lean Thinking'],
        'practice': ['Manufacturing Internships', 'Process Improvement', 'Quality Control']
    },
    'quality control': {
        'courses': [
            'https://www.coursera.org/learn/quality-management',
            'https://www.edx.org/learn/six-sigma-certification',
            'https://www.udemy.com/course/quality-control/'
        ],
        'books': ['Quality Control', 'The Six Sigma Handbook'],
        'practice': ['Quality Control Labs', 'Statistical Analysis', 'Process Auditing']
    },
    'six sigma': {
        'courses': [
            'https://www.coursera.org/learn/six-sigma-green-belt',
            'https://www.edx.org/learn/six-sigma-black-belt',
            'https://www.udemy.com/course/six-sigma/'
        ],
        'books': ['Six Sigma for Dummies', 'The Six Sigma Way'],
        'practice': ['Six Sigma Projects', 'Statistical Analysis', 'Process Improvement']
    },
    
    # Retail Skills
    'retail management': {
        'courses': [
            'https://www.coursera.org/learn/retail-management',
            'https://www.edx.org/learn/store-operations',
            'https://www.udemy.com/course/retail-management/'
        ],
        'books': ['Retail Management', 'The Retail Revolution'],
        'practice': ['Retail Internships', 'Store Management', 'Customer Service']
    },
    'visual merchandising': {
        'courses': [
            'https://www.coursera.org/learn/visual-merchandising',
            'https://www.edx.org/learn/retail-design',
            'https://www.udemy.com/course/visual-merchandising/'
        ],
        'books': ['Visual Merchandising', 'Store Design'],
        'practice': ['Store Displays', 'Window Design', 'Product Placement']
    },
    'inventory control': {
        'courses': [
            'https://www.coursera.org/learn/inventory-management',
            'https://www.edx.org/learn/supply-chain',
            'https://www.udemy.com/course/inventory-control/'
        ],
        'books': ['Inventory Management', 'Supply Chain Management'],
        'practice': ['Inventory Systems', 'Stock Management', 'Warehouse Operations']
    },
    
    # Business Skills
    'project management': {
        'courses': [
            'https://www.coursera.org/learn/project-management',
            'https://www.udemy.com/course/pmp-certification/',
            'https://www.edx.org/learn/project-management'
        ],
        'books': ['A Guide to the Project Management Body of Knowledge', 'The Fast Forward MBA in Project Management'],
        'practice': ['Project Management Software', 'Case Studies', 'Project Planning']
    },
    'leadership': {
        'courses': [
            'https://www.coursera.org/learn/leadership',
            'https://www.edx.org/learn/management-skills',
            'https://www.udemy.com/course/leadership/'
        ],
        'books': ['The Leadership Challenge', 'Good to Great'],
        'practice': ['Team Leadership', 'Mentoring', 'Leadership Roles']
    },
    'communication': {
        'courses': [
            'https://www.coursera.org/learn/business-communication',
            'https://www.edx.org/learn/public-speaking',
            'https://www.udemy.com/course/communication-skills/'
        ],
        'books': ['Crucial Conversations', 'How to Win Friends and Influence People'],
        'practice': ['Public Speaking', 'Presentation Skills', 'Interpersonal Communication']
    }
}

class CareerRecommender:
    def __init__(self):
        self.model_path = 'app/models/career_model.pkl'
        self.vectorizer_path = 'app/models/vectorizer.pkl'
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def detect_skill_gaps(self, user_skills: Dict[str, List[str]], job_required_skills: List[str]) -> List[str]:
        """Detect missing skills for a specific job"""
        user_skill_set = set()
        for category, skills in user_skills.items():
            user_skill_set.update([skill.lower() for skill in skills])
        
        missing_skills = []
        for required_skill in job_required_skills:
            if required_skill.lower() not in user_skill_set:
                missing_skills.append(required_skill)
        
        return missing_skills
    
    def calculate_job_match_score(self, user_skills: Dict[str, List[str]], job_profile: Dict, parsed_resume: Dict = None) -> float:
        """Calculate how well user skills match a job profile with CV context awareness"""
        user_skill_set = set()
        for category, skills in user_skills.items():
            user_skill_set.update([skill.lower() for skill in skills])
        
        required_skills = set([skill.lower() for skill in job_profile['required_skills']])
        preferred_skills = set([skill.lower() for skill in job_profile.get('preferred_skills', [])])
        
        # Map individual technologies to skill categories for better matching
        skill_category_mapping = {
            # Programming languages
            'python': 'programming', 'java': 'programming', 'javascript': 'programming', 'typescript': 'programming',
            'c++': 'programming', 'c#': 'programming', 'php': 'programming', 'ruby': 'programming', 'go': 'programming',
            'rust': 'programming', 'swift': 'programming', 'kotlin': 'programming', 'scala': 'programming',
            'r': 'programming', 'matlab': 'programming', 'sas': 'programming', 'stata': 'programming', 'spss': 'programming',
            
            # Web development
            'html': 'web_development', 'css': 'web_development', 'react': 'web_development', 'angular': 'web_development',
            'vue': 'web_development', 'node.js': 'web_development', 'express': 'web_development', 'django': 'web_development',
            'flask': 'web_development', 'spring': 'web_development', 'asp.net': 'web_development', 'laravel': 'web_development',
            'wordpress': 'web_development', 'drupal': 'web_development', 'jquery': 'web_development', 'bootstrap': 'web_development',
            
            # Databases
            'sql': 'databases', 'mysql': 'databases', 'postgresql': 'databases', 'mongodb': 'databases',
            'redis': 'databases', 'oracle': 'databases', 'sqlite': 'databases', 'mariadb': 'databases',
            'cassandra': 'databases', 'neo4j': 'databases', 'elasticsearch': 'databases', 'dynamodb': 'databases',
            
            # Cloud platforms
            'aws': 'cloud_platforms', 'azure': 'azure', 'gcp': 'cloud_platforms', 'google cloud': 'cloud_platforms',
            'amazon web services': 'cloud_platforms', 'docker': 'cloud_platforms', 'kubernetes': 'cloud_platforms',
            'terraform': 'cloud_platforms', 'jenkins': 'cloud_platforms', 'gitlab': 'cloud_platforms',
            
            # DevOps
            'ci/cd': 'devops', 'continuous integration': 'devops', 'continuous deployment': 'devops',
            'jenkins': 'devops', 'gitlab ci': 'devops', 'github actions': 'devops', 'docker': 'devops',
            'kubernetes': 'devops', 'terraform': 'devops', 'ansible': 'devops', 'chef': 'devops', 'puppet': 'devops',
            
            # Data science
            'machine learning': 'data_science', 'deep learning': 'data_science', 'tensorflow': 'data_science',
            'pytorch': 'data_science', 'scikit-learn': 'data_science', 'pandas': 'data_science', 'numpy': 'data_science',
            'matplotlib': 'data_science', 'seaborn': 'data_science', 'plotly': 'data_science', 'jupyter': 'data_science',
            'spark': 'data_science', 'hadoop': 'data_science', 'hive': 'data_science', 'kafka': 'data_science',
            'airflow': 'data_science', 'tableau': 'data_science', 'power bi': 'data_science',
            
            # Git
            'git': 'git', 'github': 'git', 'gitlab': 'git', 'bitbucket': 'git',
            
            # Algorithms
            'algorithms': 'algorithms', 'data structures': 'algorithms', 'sorting': 'algorithms',
            'searching': 'algorithms', 'dynamic programming': 'algorithms', 'graph algorithms': 'algorithms'
        }
        
        # Expand user skills with category mappings
        expanded_user_skills = user_skill_set.copy()
        for skill in user_skill_set:
            if skill in skill_category_mapping:
                expanded_user_skills.add(skill_category_mapping[skill])
        
        # Calculate base match scores with expanded skills
        required_match = len(expanded_user_skills.intersection(required_skills)) / len(required_skills) if required_skills else 0
        preferred_match = len(expanded_user_skills.intersection(preferred_skills)) / len(preferred_skills) if preferred_skills else 0
        
        # Base weighted score
        base_score = (required_match * 0.7) + (preferred_match * 0.3)
        
        # Apply CV context bonuses if parsed_resume is provided
        if parsed_resume:
            # Bonus for matching job titles/roles in CV
            cv_job_titles = []
            if 'experience' in parsed_resume:
                for exp in parsed_resume['experience']:
                    if isinstance(exp, str):
                        # Extract job titles from experience strings
                        if '|' in exp:
                            job_title = exp.split('|')[0].strip()
                            cv_job_titles.append(job_title.lower())
                        elif 'at' in exp.lower():
                            parts = exp.split('at')
                            if len(parts) > 1:
                                job_title = parts[0].strip()
                                cv_job_titles.append(job_title.lower())
            
            # Check if job profile title matches CV job titles
            job_title_lower = job_profile['title'].lower()
            title_match_bonus = 0.0
            
            for cv_title in cv_job_titles:
                # Check for exact or partial matches
                if job_title_lower in cv_title or cv_title in job_title_lower:
                    title_match_bonus = 0.3  # Significant bonus for matching job titles
                    break
                # Check for keyword matches (e.g., "engineer", "developer", "manager")
                title_keywords = ['engineer', 'developer', 'manager', 'analyst', 'specialist', 'coordinator', 'scientist']
                for keyword in title_keywords:
                    if keyword in job_title_lower and keyword in cv_title:
                        title_match_bonus = 0.2
                        break
                
                # Check for more specific matches
                if 'software engineer' in cv_title.lower() and 'software engineer' in job_title_lower:
                    title_match_bonus = 0.4  # Higher bonus for exact role match
                    break
                elif 'data scientist' in cv_title.lower() and 'data scientist' in job_title_lower:
                    title_match_bonus = 0.4
                    break
                elif 'marketing manager' in cv_title.lower() and 'marketing manager' in job_title_lower:
                    title_match_bonus = 0.4
                    break
                elif 'civil engineer' in cv_title.lower() and 'civil engineer' in job_title_lower:
                    title_match_bonus = 0.4
                    break
            
            # Bonus for skills mentioned in work experience
            experience_bonus = 0.0
            if 'experience' in parsed_resume:
                experience_text = ' '.join([str(exp) for exp in parsed_resume['experience']]).lower()
                experience_skills = user_skill_set.intersection(required_skills)
                if experience_skills:
                    # Calculate what percentage of required skills appear in experience
                    experience_skill_ratio = len(experience_skills) / len(required_skills) if required_skills else 0
                    experience_bonus = experience_skill_ratio * 0.2
            
            # Apply bonuses with higher weight for exact job title matches
            if title_match_bonus > 0.3:  # Exact role match
                total_score = min(1.0, base_score + title_match_bonus + experience_bonus)
            else:
                # For non-exact matches, reduce the base score to prioritize exact matches
                total_score = min(1.0, (base_score * 0.7) + title_match_bonus + experience_bonus)
            
            return total_score
        
        return base_score
    
    def get_career_recommendations(self, user_skills: Dict[str, List[str]], top_n: int = 5, parsed_resume: Dict = None) -> List[Dict]:
        """Get top career recommendations based on user skills with CV context awareness"""
        recommendations = []
        
        for job_title, job_profile in JOB_PROFILES.items():
            match_score = self.calculate_job_match_score(user_skills, job_profile, parsed_resume)
            skill_gaps = self.detect_skill_gaps(user_skills, job_profile['required_skills'])
            
            recommendations.append({
                'job_title': job_profile['title'],
                'match_score': round(match_score * 100, 2),
                'description': job_profile['description'],
                'missing_skills': skill_gaps,
                'required_skills': job_profile['required_skills'],
                'preferred_skills': job_profile.get('preferred_skills', []),
                'sector': job_profile.get('sector', 'unknown')
            })
        
        # Sort by match score (highest first)
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:top_n]
    
    def get_learning_plan(self, missing_skills: List[str]) -> Dict[str, Dict]:
        """Generate learning plan for missing skills"""
        learning_plan = {}
        
        for skill in missing_skills:
            skill_lower = skill.lower()
            if skill_lower in LEARNING_RESOURCES:
                learning_plan[skill] = LEARNING_RESOURCES[skill_lower]
            else:
                # Generic learning resources for unknown skills
                learning_plan[skill] = {
                    'courses': [f'Search for "{skill}" courses on Coursera, Udemy, or edX'],
                    'books': [f'Search for "{skill}" books on Amazon or Goodreads'],
                    'practice': ['Build projects', 'Contribute to open source', 'Join communities']
                }
        
        return learning_plan
    
    def get_skill_analysis(self, user_skills: Dict[str, List[str]]) -> Dict:
        """Analyze user skills and provide insights"""
        total_skills = sum(len(skills) for skills in user_skills.values())
        skill_categories = list(user_skills.keys())
        
        # Find strongest category
        strongest_category = max(user_skills.items(), key=lambda x: len(x[1]))[0] if user_skills else None
        
        # Find most in-demand skills
        all_user_skills = []
        for category, skills in user_skills.items():
            all_user_skills.extend(skills)
        
        # Check against high-demand skills
        high_demand_skills = ['python', 'javascript', 'sql', 'aws', 'docker', 'react', 'machine learning']
        in_demand_skills = [skill for skill in all_user_skills if skill.lower() in high_demand_skills]
        
        return {
            'total_skills': total_skills,
            'skill_categories': skill_categories,
            'strongest_category': strongest_category,
            'in_demand_skills': in_demand_skills,
            'skill_diversity_score': len(skill_categories) / 6  # Normalize by max categories
        }
    
    def get_personalized_advice(self, user_skills: Dict[str, List[str]], recommendations: List[Dict]) -> Dict:
        """Generate personalized career advice"""
        skill_analysis = self.get_skill_analysis(user_skills)
        top_recommendation = recommendations[0] if recommendations else None
        
        advice = {
            'current_position': 'Based on your skills, you appear to be in a good position for:',
            'next_steps': [],
            'skill_gaps': [],
            'market_insights': []
        }
        
        if top_recommendation:
            if top_recommendation['match_score'] >= 80:
                advice['current_position'] = f"You're well-qualified for {top_recommendation['job_title']} roles!"
                advice['next_steps'].append(f"Focus on gaining experience in {top_recommendation['job_title']} positions")
                advice['next_steps'].append("Build a portfolio showcasing your projects")
            elif top_recommendation['match_score'] >= 60:
                advice['current_position'] = f"You have a good foundation for {top_recommendation['job_title']} roles"
                advice['next_steps'].append(f"Learn the missing skills: {', '.join(top_recommendation['missing_skills'][:3])}")
                advice['next_steps'].append("Take relevant courses and certifications")
            else:
                advice['current_position'] = "You may need to develop more skills for your target roles"
                advice['next_steps'].append("Focus on building core technical skills")
                advice['next_steps'].append("Consider entry-level positions to gain experience")
        
        # Add skill-specific advice
        if skill_analysis['in_demand_skills']:
            advice['market_insights'].append(f"Great! You have in-demand skills: {', '.join(skill_analysis['in_demand_skills'])}")
        
        if skill_analysis['skill_diversity_score'] < 0.5:
            advice['skill_gaps'].append("Consider diversifying your skill set across different domains")
        
        return advice

def get_recommendations(parsed_resume: Dict) -> Dict:
    """Main function to get career recommendations"""
    recommender = CareerRecommender()
    user_skills = parsed_resume.get('skills', {})
    
    # Get career recommendations with CV context awareness
    recommendations = recommender.get_career_recommendations(user_skills, parsed_resume=parsed_resume)
    
    # Get learning plan for top recommendation
    top_recommendation = recommendations[0] if recommendations else None
    learning_plan = {}
    if top_recommendation:
        learning_plan = recommender.get_learning_plan(top_recommendation['missing_skills'])
    
    # Get skill analysis and advice
    skill_analysis = recommender.get_skill_analysis(user_skills)
    personalized_advice = recommender.get_personalized_advice(user_skills, recommendations)
    
    return {
        'recommendations': recommendations,
        'learning_plan': learning_plan,
        'skill_analysis': skill_analysis,
        'personalized_advice': personalized_advice
    } 