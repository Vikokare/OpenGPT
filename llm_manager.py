import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.7,
)