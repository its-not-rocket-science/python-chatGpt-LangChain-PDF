import os
from pinecone import Pinecone as PineconeClient
from langchain.vectorstores.pinecone import Pinecone
from app.chat.embeddings.openai import embeddings
from app.chat.models import ChatArgs

PineconeClient(
    api_key=os.getenv("PINECONE_API_KEY")
)

vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"),
    embeddings
)


def build_retriever(chat_args: ChatArgs, k: int):
    search_kwargs = {
        "filter": {"pdf_id": chat_args.pdf_id},
        "k": k
    }
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )
