import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent

from tools import tools
import prompts

load_dotenv()


class LLMService:
    def __init__(self, model="llama3-8b-8192"):
        self.model = model
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def set_model(self, model):
        self.model = model

    async def generate(self, message: str, model: str = None) -> str:
        llm = ChatGroq(
            model=model or self.model,
            temperature=0.7,
        )

        chat_history = self.memory.load_memory_variables({}).get("chat_history", [])

        agent = initialize_agent(
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            tools=tools,
            llm=llm,
            prompt=prompts.main_prompt,
            memory=self.memory,
            input_key="input",
        )

        response = agent({"input": message, "chat_history": chat_history})
        return response["output"]

    async def generate_starters(self, model: str = None) -> str:
        llm = ChatGroq(
            model=model,
            temperature=0.7,
        )

        prompt_template = PromptTemplate(input_variables=[], template=prompts.main_prompt)
        llm_chain = LLMChain(prompt=prompt_template, llm=llm)

        # Get starter topics response from Groq (simulating with OpenAI here for simplicity)
        starters_response = llm_chain.run({})
        print(starters_response)
