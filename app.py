import streamlit as st
import base64
import os
import io
from typing import Optional, List, Dict
from dataclasses import dataclass
from PIL import Image 
import pdf2image
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
genai.configure(api_key=GOOGLE_API_KEY)

@dataclass
class PDFContent:
    """Data class to store PDF content information"""
    mime_type: str
    data: str

from datetime import datetime, timedelta
import time
from collections import deque

class RateLimiter:
    """Handles API rate limiting"""
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests  # Maximum requests allowed
        self.time_window = time_window    # Time window in seconds
        self.requests = deque()           # Queue to track request timestamps
        
    def wait_if_needed(self):
        """Check if we need to wait before making another request"""
        now = datetime.now()
        
        # Remove old requests from queue
        while self.requests and self.requests[0] < now - timedelta(seconds=self.time_window):
            self.requests.popleft()
        
        # If we've hit the rate limit, wait
        if len(self.requests) >= self.max_requests:
            wait_time = (self.requests[0] + timedelta(seconds=self.time_window) - now).total_seconds()
            if wait_time > 0:
                st.warning(f"Rate limit reached. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        
        # Add current request to queue
        self.requests.append(now)

class ATSAnalyzer:
    """Class to handle ATS resume analysis"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        # Initialize rate limiter: 15 requests per minute
        self.rate_limiter = RateLimiter(max_requests=15, time_window=60)
        
    @staticmethod
    def process_pdf(uploaded_file) -> List[Dict[str, str]]:
        """Process uploaded PDF file and convert to required format"""
        try:
            images = pdf2image.convert_from_bytes(
                uploaded_file.read(),
                poppler_path=r"C:/Program Files/poppler/Library/bin"
            )
            
            first_page = images[0]
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return [{
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }]
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return None
    
    def get_analysis(self, input_prompt: str, pdf_content: List[Dict[str, str]], job_description: str) -> str:
        """Get analysis from Gemini model"""
        try:
            # Check rate limit before making request
            self.rate_limiter.wait_if_needed()
            
            # Make the API call
            response = self.model.generate_content([input_prompt, pdf_content[0], job_description])
            return response.text
        except Exception as e:
            st.error(f"Error getting analysis: {str(e)}")
            return None

class ATSApp:
    """Main Streamlit application class"""
    
    def __init__(self):
        self.analyzer = ATSAnalyzer()
        self.setup_prompts()
        
    def setup_prompts(self):
        """Setup analysis prompts with improved instructions"""
        self.prompts = {
            "resume_analysis": """
            As an experienced Technical Human Resource Manager with expertise in [JOB_FIELD], conduct a comprehensive review of the resume against the job description. Please provide a structured analysis including:

            1. Overall Alignment (Scale 1-10)
            2. Key Strengths:
               - Technical skills that match perfectly
               - Relevant experience highlights
               - Notable achievements
            3. Areas for Development:
               - Missing critical skills
               - Experience gaps
               - Suggested improvements
            4. Specific Recommendations:
               - Skills to acquire
               - Certifications to pursue
               - Projects to undertake
            
            Please be specific and provide actionable feedback that will help the candidate improve their profile for this role.
            """,
            
            "skills_improvement": """
            As an experienced Career Coach specializing in [JOB_FIELD], analyze the resume and job description to provide:

            1. Skill Gap Analysis:
               - Critical missing skills
               - Emerging technologies not mentioned
               - Industry-specific knowledge gaps
            
            2. Detailed Learning Path:
               - Recommended online courses
               - Certification priorities
               - Hands-on project suggestions
               - Timeline for skill acquisition
            
            3. Career Development Strategy:
               - Short-term goals (3-6 months)
               - Long-term goals (1-2 years)
               - Industry networking suggestions
            
            Provide specific, actionable recommendations with estimated timelines for implementation.
            """,
            
            "match_analysis": """
            As an advanced ATS scanner with expertise in [JOB_FIELD], provide a detailed analysis including:

            1. Overall Match Score:
               - Percentage match with explanation
               - Breakdown by category (skills, experience, education)
            
            2. Keyword Analysis:
               - Present keywords (weighted by importance)
               - Missing critical keywords
               - Context analysis of keyword usage
            
            3. ATS Optimization Recommendations:
               - Format improvements
               - Keyword placement suggestions
               - Content enhancement opportunities
            
            4. Competitive Analysis:
               - Position in candidate pool
               - Stand-out qualifications
               - Critical differentiators needed
            
            Provide specific examples and actionable recommendations for improvement.
            """
        }
    
    def run(self):
        """Run the Streamlit application"""
        st.set_page_config(page_title="Advanced ATS Resume Expert")
        st.title("Advanced ATS Resume Analysis System")
        
        # Job Description Input
        job_description = st.text_area(
            "Job Description:",
            help="Paste the complete job description here",
            height=200
        )
        
        # Resume Upload
        uploaded_file = st.file_uploader(
            "Upload your Resume (PDF)",
            type=["pdf"],
            help="Please ensure your resume is in PDF format"
        )
        
        if uploaded_file:
            st.success("✅ Resume uploaded successfully")
            pdf_content = self.analyzer.process_pdf(uploaded_file)
            
            # Analysis Options
            analysis_type = st.radio(
                "Select Analysis Type:",
                ["Complete Resume Analysis", "Skills Improvement Plan", "ATS Match Score"]
            )
            
            if st.button("Analyze Resume"):
                if not job_description:
                    st.warning("Please provide a job description")
                    return
                    
                with st.spinner("Analyzing your resume..."):
                    if analysis_type == "Complete Resume Analysis":
                        prompt = self.prompts["resume_analysis"]
                    elif analysis_type == "Skills Improvement Plan":
                        prompt = self.prompts["skills_improvement"]
                    else:
                        prompt = self.prompts["match_analysis"]
                    
                    # Replace placeholder with actual job field
                    job_field = self.extract_job_field(job_description)
                    prompt = prompt.replace("[JOB_FIELD]", job_field)
                    
                    response = self.analyzer.get_analysis(prompt, pdf_content, job_description)
                    if response:
                        st.markdown("### Analysis Results")
                        st.markdown(response)
                        
                        # Add download button for the analysis
                        st.download_button(
                            "Download Analysis",
                            response,
                            file_name="resume_analysis.txt",
                            mime="text/plain"
                        )
    
    @staticmethod
    def extract_job_field(job_description: str) -> str:
        """Extract the job field from the job description"""
        # This could be enhanced with better field detection logic
        common_fields = ["Data Science", "Software Engineering", "Data Engineering", 
                        "Machine Learning", "DevOps", "Cloud Engineering"]
        for field in common_fields:
            if field.lower() in job_description.lower():
                return field
        return "Technology"

if __name__ == "__main__":
    app = ATSApp()
    app.run()