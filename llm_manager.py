import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# prompt = ChatPromptTemplate.from_template(
#     """
#     You are an AI assistant designed to provide information and answer questions in a polite and respectful manner. 
#     Your goal is to assist users by delivering accurate, relevant, and concise responses while maintaining a friendly and approachable tone. 
#     Always acknowledge the user's request and provide clear explanations or solutions. 
#     If you're unsure about something, it's okay to express that and encourage the user to ask further questions. 
#     Remember to prioritize user satisfaction and foster a positive interaction.
    
#     Question: {question}
#     """
# )

prompt = ChatPromptTemplate.from_template(
    """
    You are an AI assistant designed to provide information and answer questions in a polite and respectful manner. 
    Your goal is to assist users by delivering accurate, relevant, and concise responses while maintaining a friendly and approachable tone. 
    
    Question: {question}
    """
)


def llm_response(message, model="llama3-8b-8192"):

    llm = ChatGroq(
        model=model,
        temperature=0.7,
    )

    chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    response = chain.invoke({
        "question": message.content
    })      
    # print("RESPONSE:", response)

    return response