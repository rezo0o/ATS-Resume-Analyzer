# ATS Resume Analyzer

An AI-powered resume screening system that analyzes resumes against job descriptions using Google's Gemini API.

## Features
- Resume analysis against job descriptions
- Skills improvement recommendations
- ATS match scoring
- PDF processing capability

## Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your Google API key
6. Run the app: `streamlit run app.py`

## Requirements
- Python 3.8+
- Poppler (for PDF processing)
- Google API key for Gemini

## Environment Variables
Create a `.env` file with: