import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.agents import AgentType, Tool, initialize_agent

from tools import tools
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


prompt = PromptTemplate(
    input_variables=["input", "chat_history"],
    template=
        """
            Question: {input}
            History: {chat_history}
            Let's think step-by-step. Analyze the problem, check any needed references, and provide a detailed response.
        """,
)

plan_prompt = PromptTemplate(
    input_variables=["input", "chat_history"],
    template=
        """
            Plan execution: Prepare a step-by-step breakdown of tasks. Example: (1) Check tools (e.g., Wikipedia, Web Search); (2) Gather info if relevant.\n\n
            Question: {input}
            History: {chat_history}
        """,
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

async def llm_response(message, model):

    llm = ChatGroq(
        model=model,
        temperature=0.7,
    )

    main_prompt = PromptTemplate(
        template="""
            You are an AI assistant focused on accurate and relevant information retrieval.
    
            - If the user’s query relates to previous interactions or requires recall (like remembering a name), respond based on memory only.
            - Only use web tools if the question requires current or factual data unavailable in your memory.
            
            Question: {input}
            History: {chat_history}
            
            Let's answer precisely, without external tools unless the query needs it.
        """,
        input_variables=["input", "chat_history"],
    )

    chat_history = memory.load_memory_variables({}).get("chat_history", [])

    agent = initialize_agent(
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        prompt=main_prompt,
        memory=memory,
        input_key="input",
    )


    response = agent({"input": message, "chat_history": chat_history})
    return response["output"]