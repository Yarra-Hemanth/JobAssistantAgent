from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from resume_utils import score_resume, answer_question
from jd_utils import extract_job_description
from extract_utils import extract_resume
from fastapi import APIRouter

session_data = {
    "resume_text": None,
    "jd_text": None
}


app = FastAPI()

# Existing JSON-based models
class ResumeRequest(BaseModel):
    jd_text: str
    resume_text: str

class QuestionRequest(BaseModel):
    jd_text: str
    resume_text: str
    question: str


@app.post("/upload-inputs")
async def upload_inputs(
    resume_file: UploadFile = File(...),
    jd_url: str = Form(None),            # ✅ now optional
    jd_manual: str = Form("")            # optional as before
):
    resume_text = await extract_resume(resume_file)

    jd_text = extract_job_description(jd_url) if jd_url else ""

    from resume_utils import is_jd_valid

    if not is_jd_valid(jd_text):
        if not jd_manual or len(jd_manual.strip()) < 20:
            return JSONResponse(
                status_code=400,
                content={"error": "Unable to extract JD from URL. Please provide JD manually."}
            )
        jd_text = jd_manual

    session_data["resume_text"] = resume_text
    session_data["jd_text"] = jd_text

    return {"message": "✅ Resume and JD successfully uploaded and stored."}



@app.post("/score-resume")
def score_from_session():
    if not session_data.get("resume_text") or not session_data.get("jd_text"):
        return JSONResponse(status_code=400, content={"error": "Missing resume or JD. Please upload them first via /upload-inputs."})

    result = score_resume(session_data["jd_text"], session_data["resume_text"])
    
    if isinstance(result, dict) and "error" in result:
        return JSONResponse(status_code=500, content=result)
    
    return JSONResponse(status_code=200, content={"result": result})


class Question(BaseModel):
    question: str

@app.post("/answer-question")
def answer_from_session(q: Question):
    if not session_data.get("resume_text") or not session_data.get("jd_text"):
        return JSONResponse(status_code=400, content={"error": "Missing resume or JD. Please upload them first via /upload-inputs."})

    answer = answer_question(session_data["jd_text"], session_data["resume_text"], q.question)

    if isinstance(answer, dict) and "error" in answer:
        return JSONResponse(status_code=500, content=answer)

    return JSONResponse(status_code=200, content=answer)
