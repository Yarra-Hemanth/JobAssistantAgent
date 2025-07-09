from models.groq_client import client
# from models.groq_client import ask_groq
from extract_utils import extract_resume
# from jd_utils import scrape_jd_from_url

# resume_text = extract_resume("path/to/resume.pdf")
# jd_text = scrape_jd_from_url("https://somejobsite.com/job/123")

import json
import re

def score_resume(jd_text, resume_text):
    if not jd_text or not resume_text:
        return {"error": "Invalid input. JD and Resume text must be provided."}

    prompt = f"""
    You are a job assistant. Compare the following resume with the job description.
    Return **only** a valid JSON object with two keys:
    - "score": an integer between 0 and 100
    - "suggestions": an array of strings

    Format:
    {{
      "score": 85,
      "suggestions": ["Add metrics", "Highlight Python projects"]
    }}

    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        print("🧠 Raw model output:", content)

        # Extract the first JSON object from the text
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
            if "score" in parsed and isinstance(parsed["score"], int) and \
               "suggestions" in parsed and isinstance(parsed["suggestions"], list):
                return parsed
            else:
                return {"error": "Invalid JSON keys or structure."}
        else:
            return {"error": "No JSON object found in model output."}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}


def answer_question(jd_text, resume_text, question):
    if not jd_text or not resume_text or not question:
        return {"error": "JD, resume, and question must all be provided."}

    prompt = f"""
    You are an expert career coach. Based on the following resume and job description, write a compelling, concise, and personalized answer to the application question. Use a professional yet enthusiastic tone.

    Resume:
    {resume_text}

    Job Description:
    {jd_text}

    Application Question:
    {question}

    Your Answer:
    """

    try:
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "answer": response.choices[0].message.content.strip()
        }
    except Exception as e:
        return {
            "error": f"Exception occurred: {str(e)}"
        }
