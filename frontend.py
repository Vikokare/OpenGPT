import chainlit as cl

from langchain_community.document_loaders import PyPDFLoader

from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

# from pinecone import Pinecone, ServerlessSpec
# from langchain_pinecone import PineconeVectorStore
# import pinecone

import os
from dotenv import load_dotenv
load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


# embedding_model_1 = HuggingFaceEmbeddings(
#     model_name="all-MiniLM-L6-v2"
# )

# pc = Pinecone(api_key=PINECONE_API_KEY)

# index_name = "book-sync"
# if index_name not in pc.list_indexes().names():
#     pc.create_index(
#         name=index_name,
#         dimension=384,
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud='aws',
#             region='us-east-1'
#         )
#     )
#     print("Created index...\n", pc.describe_index(index_name))
# else:
#     print("Index already exists")

# index = pc.Index(index_name)

# Create instance without doc
# docsearch_instance = PineconeVectorStore(
#     pinecone_api_key=PINECONE_API_KEY,
#     embedding=embedding_model_1,
#     index=index,
# )


# Function to get similar data
def get_similar_doc(query, k=3, score=True):
    if score:
        similar_docs = docsearch.similarity_search_with_score(query, k=k)
    else:
        similar_docs = docsearch.similarity_search(query, k=k)
    return similar_docs


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Summarize Books",
            message="Help me summarize a refrence book",
            icon="./public/icons8-student-male-100.png",
        ),

        cl.Starter(
            label="Data Scientist",
            message="search for ...",
            icon="./public/icons8-student-male-50.png",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    ...


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
        print("DOCS:", pages[1:10])
        
        # # Create instance -> embed doc and upsert
        # docsearch = PineconeVectorStore.from_documents(
        #     pinecone_api_key=PINECONE_API_KEY,
        #     index_name=index_name,
        #     embedding=embedding_model_1,
        #     documents=docs,
        # )


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