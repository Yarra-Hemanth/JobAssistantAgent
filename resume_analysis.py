from models.groq_client import client
from file_extractors import extract_resume
import json
import re

def is_jd_valid(jd_text):
    if not jd_text or len(jd_text.split()) < 75:
        return False
    if any(kw in jd_text.lower() for kw in [
        "cloudflare", "security service", "this website is using a security service",
        "slide 1 of", "blocked", "invalid request", "access denied"
    ]):
        return False
    return True

def score_resume(jd_text, resume_text):
    if not jd_text or not resume_text:
        return {"error": "Invalid input. JD and Resume text must be provided."}

    if not is_jd_valid(jd_text):
        return {
            "score": 0,
            "suggestions": ["Invalid JD. Please enter the JD manually or use another link."]
        }

    prompt = f"""
            You are a job assistant. Compare the following resume with the job description.

            If the job description appears suspicious or incomplete (e.g., marketing text, empty content, or bot protection messages),
            assign a lower score (e.g., 10–30) and explain why in the suggestions.
            Otherwise, score the resume normally based on its match to the JD.

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
        print("Raw model output:", content)

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
