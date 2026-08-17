from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="openai/gpt-oss-20b") #type: ignore
