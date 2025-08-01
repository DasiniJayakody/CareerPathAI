from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os
from typing import Dict, Any
import uvicorn

from services.resume_parser import parse_resume, parse_resume_text
from services.career_recommender import get_recommendations

app = FastAPI(
    title="CareerPathAI API",
    description="AI-powered career guidance system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CareerPathAI API",
        "version": "1.0.0",
        "endpoints": {
            "/upload_resume": "Upload and parse resume",
            "/parse_text": "Parse resume from text",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CareerPathAI"}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume file (PDF or DOCX)
    """
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.docx']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Please upload a PDF or DOCX file."
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            # Write uploaded file to temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse the resume
            parsed_data = parse_resume(temp_file_path)
            
            # Get career recommendations
            recommendations = get_recommendations(parsed_data)
            
            # Combine results
            result = {
                "parsed_resume": parsed_data,
                "career_analysis": recommendations,
                "file_info": {
                    "filename": file.filename,
                    "file_size": len(content),
                    "file_type": file_extension
                }
            }
            
            return JSONResponse(content=result)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )

@app.post("/parse_text")
async def parse_text_resume(resume_text: str = Form(...)):
    """
    Parse resume from text input
    """
    try:
        # Parse the resume text
        parsed_data = parse_resume_text(resume_text)
        
        # Get career recommendations
        recommendations = get_recommendations(parsed_data)
        
        # Combine results
        result = {
            "parsed_resume": parsed_data,
            "career_analysis": recommendations
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume text: {str(e)}"
        )

@app.post("/analyze_skills")
async def analyze_skills(skills_data: Dict[str, Any]):
    """
    Analyze skills and get career recommendations without resume parsing
    """
    try:
        # Create a mock parsed resume with skills
        mock_parsed_resume = {
            "skills": skills_data.get("skills", {}),
            "name": skills_data.get("name", "User"),
            "email": skills_data.get("email", ""),
            "phone": skills_data.get("phone", "")
        }
        
        # Get career recommendations
        recommendations = get_recommendations(mock_parsed_resume)
        
        return JSONResponse(content={
            "career_analysis": recommendations,
            "input_skills": skills_data
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing skills: {str(e)}"
        )

@app.get("/job_profiles")
async def get_job_profiles():
    """
    Get available job profiles and their requirements
    """
    from services.career_recommender import JOB_PROFILES
    
    return JSONResponse(content={
        "job_profiles": JOB_PROFILES,
        "total_profiles": len(JOB_PROFILES)
    })

@app.get("/learning_resources")
async def get_learning_resources():
    """
    Get available learning resources
    """
    from services.career_recommender import LEARNING_RESOURCES
    
    return JSONResponse(content={
        "learning_resources": LEARNING_RESOURCES,
        "total_skills": len(LEARNING_RESOURCES)
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 