# 💼 Job Assistant Agent

An AI-powered resume evaluation and job description analysis tool built with FastAPI. It scores resumes against job descriptions, answers application questions, and supports resume/JD upload via file or URL.

## 🚀 Features

- ✅ Upload resume (`PDF`, `DOCX`, `TXT`) and job description via URL or manual input
- ✅ Intelligent resume scoring using LLMs (LLaMA 3 & Mistral)
- ✅ Application question answering based on resume and JD
- ✅ Web scraping from popular job portals (LinkedIn, Indeed, Naukri, etc.)
- ✅ Supports fallback extraction using Goose, Newspaper3k, Readability
- ✅ Easy integration with frontend or automation tools

---

## 📁 Project Structure

JobAssistantAgent/
├── app.py # FastAPI backend with endpoints  
├── resume_analysis.py # Resume scoring and QA logic  
├── jd_extraction.py # Job description scraping/extraction  
├── file_extractors.py # Resume text extraction handlers  
├── models/  
│ └── groq_client.py # LLM client setup (e.g., GROQ API)  
├── extracted_jd.txt # Temporary storage for extracted JD (debug)  
└── requirements.txt # Python dependencies  

---

## 🔧 Installation

### 1. Clone the repository
git clone https://github.com/Yarra-Hemanth/JobAssistantAgent.git  
cd JobAssistantAgent

### 2. Create and activate a virtual environment
python -m venv venv  
source venv/bin/activate    # On Windows: venv\Scripts\activate

### 3. Install dependencies
  pip install -r requirements.txt  
  
### 4. Install ChromeDriver (⚠ Required for JD extraction from URL)
Download undetected-chromedriver and ensure Chrome is installed on your system.
📎 **Note:** Error handling and setup instructions for ChromeDriver are provided in [`ChromeDriver_Setup_Guide.md`](./ChromeDriver_Setup_Guide.md).


▶️ Running the App
uvicorn app:app --reload  # Here the initial app indicates the app.py file.

Visit http://127.0.0.1:8000/docs to access the Swagger API documentation.

📬 API Endpoints
1. /upload-inputs – Upload resume and JD
Method: POST (multipart/form-data)
Parameters:  
resume_file: Resume file (PDF, DOCX, or TXT)  
jd_url: (Optional) URL of the job description  
jd_manual: (Optional) Manual JD text (fallback)  

2. /score-resume – Score based on last uploaded resume and JD
Method: POST
Response:
{  
  "score": 85,  
  "suggestions": ["Add metrics", "Highlight Python projects"]  
}

3. /answer-question – Answer a job application question
Method: POST
Body:
{  
  "question": "Why do you want to work with us?"  
}

🧠 Powered by
FastAPI  
GROQ  
LLaMA 3  
Mistral  
Selenium + undetected_chromedriver  
Newspaper3k  
Readability  
Goose3

📌 To-Do
 Add frontend UI (React or Streamlit)
 Add authentication (JWT/session-based)
 Improve resume parsing with NLP
 Dockerize the project for deployment

🤝 Contributing
Pull requests are welcome! Please open an issue first to discuss what you'd like to change.

🛡 License
This project is licensed under the MIT License.

🙋‍♂️ Author
Hemanth Yarra
LinkedIn | GitHub
