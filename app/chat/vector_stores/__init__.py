from functools import partial
from .pinecone import build_retriever

retriever_registry = {
    "pinecone-1": partial(build_retriever, k=1),
    "pinecone-2": partial(build_retriever, k=2),
    "pinecone-3": partial(build_retriever, k=3)
}
