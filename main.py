from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from resume_utils import score_resume, answer_question
from jd_utils import extract_job_description
from extract_utils import extract_resume

app = FastAPI()

# Existing JSON-based models
class ResumeRequest(BaseModel):
    jd_text: str
    resume_text: str

class QuestionRequest(BaseModel):
    jd_text: str
    resume_text: str
    question: str

# ✅ Existing endpoint 1: Score resume
@app.post("/score-resume")
def score(resume_req: ResumeRequest):
    result = score_resume(resume_req.jd_text, resume_req.resume_text)
    return {"result": result}

# ✅ Existing endpoint 2: Answer JD question
@app.post("/answer-question")
def answer(req: QuestionRequest):
    answer = answer_question(req.jd_text, req.resume_text, req.question)
    return {"answer": answer}

# ✅ New endpoint 3: Upload resume file + JD URL
@app.post("/score-from-inputs")
async def score_from_inputs(
    resume_file: UploadFile = File(...),
    jd_url: str = Form(...)
):
    # Extract from file
    resume_text = extract_resume(resume_file)

    # Extract from URL
    jd_text = extract_job_description(jd_url)

    # Basic error handling
    if "Unsupported" in resume_text or "Error" in jd_text:
        return JSONResponse(status_code=400, content={"error": "Invalid file or URL"})

    result = score_resume(jd_text, resume_text)
    return {"result": result}
