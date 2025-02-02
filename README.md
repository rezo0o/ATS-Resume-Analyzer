# ATS Resume Analyzer

An AI-powered resume screening system that analyzes resumes against job descriptions using Google's Gemini API. The system provides detailed feedback, skill gap analysis, and ATS-friendly recommendations to help job seekers optimize their resumes.

## Features

- **Resume Analysis**: Comprehensive evaluation of your resume against specific job descriptions
- **Skills Gap Assessment**: Identifies missing critical skills and provides improvement recommendations
- **ATS Match Scoring**: Detailed scoring and keyword analysis for ATS optimization
- **Multi-Environment Support**: Works both locally and on Streamlit Cloud
- **PDF Processing**: Efficient handling of PDF resumes
- **Downloadable Reports**: Get detailed analysis reports in text format

## Live Demo

Try the live demo: [ATS Resume Analyzer on Streamlit](https://ats-resume-analyzer-rezo0o.streamlit.app/)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git
- Google API key for Gemini (Get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
- For local development on Windows: Poppler (included in requirements for other platforms)

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ats-resume-analyzer.git
cd ats-resume-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Unix/MacOS:
  ```bash
  source venv/bin/activate
  ```

4. Install required packages:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
- Create a `.env` file in the project root
- Add your Google API key:
  ```
  GOOGLE_API_KEY=your_api_key_here
  ```

6. Run the application:
```bash
streamlit run app.py
```

### Windows-Specific Setup

If you're developing on Windows, you'll need to install Poppler:
1. Download Poppler from [here](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract it to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to your system's PATH

## Project Structure

```
ats-resume-analyzer/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── packages.txt          # System dependencies for Streamlit Cloud
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## Dependencies

Key dependencies include:
- streamlit
- pdf2image
- google-generativeai
- poppler-utils-binary
- python-dotenv
- Pillow

Full list available in `requirements.txt`

### System Dependencies (Streamlit Cloud)
Create a `packages.txt` file with:
```
poppler-utils
```

This ensures proper PDF processing functionality on Streamlit Cloud.

## Environment Variables

Create a `.env` file with the following:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage

1. Upload your resume in PDF format
2. Paste the job description you're targeting
3. Select the type of analysis you want:
   - Complete Resume Analysis
   - Skills Improvement Plan
   - ATS Match Score
4. Click "Analyze Resume" to get detailed feedback
5. Download the analysis report if needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) for details.

## Acknowledgments

- Google Gemini API for providing the AI capabilities
- Streamlit for the web framework
- PDF2Image and Poppler for PDF processing

## Contact

For any queries or suggestions, please open an issue in the repository.

---
Built with using Streamlit and Google Gemini