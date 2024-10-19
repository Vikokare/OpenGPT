import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def llm_response(message):
    llm = ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0.7,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", 
                "You are a helpful assistant designed to assist users with their queries. "
                "Your goal is to provide accurate and concise information while maintaining a friendly and engaging tone. "
                "You can answer questions, provide explanations, and assist with problem-solving. "
                "If you don't know the answer, it's okay to say that you don't know, but you can suggest where the user might find more information. "
                "Always ask clarifying questions if the user's request is ambiguous. "
                "Remember to be polite and patient.",
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    response = chain.invoke({"input": message})

    print("RESPONE", response)
    return response