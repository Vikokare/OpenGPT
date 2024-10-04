import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
from typing import Optional

import torch

from langchain_community.document_loaders import PyPDFLoader

from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

from langchain_chroma import Chroma 
from uuid import uuid4

import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs={'device': device})

vector_store = Chroma(
    collection_name="example-collection",
    embedding_function=embedding,
    persist_directory="./chroma_langchain_db",
)

def get_similar_doc(query, k=3, score=True):
    if score:
        similar_docs = docsearch_instance.similarity_search_with_score(query, k=k)
    else:
        similar_docs = docsearch_instance.similarity_search(query, k=k)
    return similar_docs


# Simulated user storage (replace with a database in a real application)
users_db = {
    "vaibhav": {"password": "123", "role": "ADMIN"},
}


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    print(username, password)
    user = users_db.get(username)
    if user and user["password"] == password:
        return cl.User(identifier=username, metadata={"role": user["role"]})
    return None


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Summarize Books",
            message="Help me summarize a refrence book",
            icon="./public/scholar_icon.png",
        ),

        cl.Starter(
            label="Data Scientist",
            message="Research topic ___",
            icon="./public/idea_icon.png",
        ),

        cl.Starter(
            label="Crawler",
            message="Crawl for ___",
            icon="./public/icons8-flame-64.png",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    app_user = cl.user_session.get("user")
    # await cl.Message(f"Hello {app_user.identifier}").send()

    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Model",
                values=[
                    "mixtral-8x7b-32768", 
                    "llama3-70b-8192", 
                    "llama3-8b-8192"
                ],
                initial_index=0,
            ),
            Switch(
                id="Streaming", 
                label="Streaming", 
                initial=True
            ),
            Slider(
                id="Temperature",
                label="Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()


@cl.on_settings_update
async def settings_update(settings):
    print(settings)
    print("settings Updated;;")


@cl.on_message
async def on_message(message: cl.Message):
    if message.content == "Help me summarize a refrence book":        
        files = await cl.AskFileMessage(
            content= "Please upload a file!",
            accept= ["text/plain", "application/pdf"],
            max_files=2,
            max_size_mb=100,
            timeout=60
        ).send()

        print(files)

        await cl.Message(
            content=f"{files[0].name} is successfully uploaded"
        ).send()
        
        loader = PyPDFLoader(files[0].path)
        pages = loader.load_and_split()
        


        print("Uploading doc done!")
        return None
    
    elif message.content == "Crawl for ___":
        elements = [
            cl.Pdf(
                name="pdf1", 
                display="inline", 
                path="D:/BSC-CS Vaibhav/SEMISTER V/Linux Server Administration/ubuntu-server-guide-2022-08-03.pdf"
            )
        ]

        cl.Message(
            content="Look at this local pdf!", 
            elements=elements
        ).send()



    similar_docs = get_similar_doc(message.content, k=1)
    await cl.Message(
        content=similar_docs
    ).send()


@cl.on_stop
async def on_stop():
    await cl.Message(
        content="Chat Interrupted!"
    ).send()
    


@cl.on_chat_end
async def on_chat_end():
    await cl.Message(
        content="Thank You!"
    ).send()



# Implement ChromaDB
# Use User session and chat presistent
# Seperate code logic
# Use GPU for compuatation