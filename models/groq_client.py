from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="D:/Desktop/JobAssistantAgent/.env")
# print("🔑 Loaded key:", os.getenv("GROQ_API_KEY"))


load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
