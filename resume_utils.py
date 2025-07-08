from models.groq_client import client
# from models.groq_client import ask_groq
from extract_utils import extract_resume
# from jd_utils import scrape_jd_from_url

# resume_text = extract_resume("path/to/resume.pdf")
# jd_text = scrape_jd_from_url("https://somejobsite.com/job/123")

def score_resume(jd_text, resume_text):
    prompt = f"""
You are a job assistant. Compare the following resume with the job description. 
Give a matching score out of 100 and suggestions to improve.

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def answer_question(jd_text, resume_text, question):
    prompt = f"""
Based on the following resume and job description:

Resume:
{resume_text}

Job Description:
{jd_text}

Answer this question:
{question}
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
