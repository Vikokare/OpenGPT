import torch
from langchain_chroma import Chroma 
# from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from uuid import uuid4
from transformers import AutoModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model.save_pretrained('./models/all-MiniLM-L6-v2')

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2", 
    model_kwargs={'device': device}
)

vector_store = Chroma(
    collection_name="example-collection",
    embedding_function=embedding_model,
    persist_directory="./chroma_langchain_db",
)

def embed_docs(docs):
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)


def retrive_docs(query):    
    results = vector_store.similarity_search(query, k=2 )

    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")


def get_similar_doc(query, k=3, score=True):
    if score:
        similar_docs = docsearch_instance.similarity_search_with_score(query, k=k)
    else:
        similar_docs = docsearch_instance.similarity_search(query, k=k)
    return similar_docs