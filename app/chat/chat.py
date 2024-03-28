from langchain_openai import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_registry
from app.chat.llms import llm_registry
from app.chat.memories import memory_registry
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import (
    get_conversation_components,
    set_conversation_components
)
from app.chat.score import weighted_random_component_by_score


def select_component(
    component_type: str,
    component_registry: dict[str, str],
    chat_args: ChatArgs
):
    components = get_conversation_components(chat_args.conversation_id)
    component_name = components[component_type]

    if not component_name:
        component_name = weighted_random_component_by_score(
            component_type,
            component_registry
        )

    return component_name, component_registry[component_name](chat_args)


def build_chat(chat_args: ChatArgs) -> StreamingConversationalRetrievalChain:
    retriever_name, retriever = select_component(
        "retriever",
        retriever_registry,
        chat_args
    )
    llm_name, llm = select_component(
        "llm",
        llm_registry,
        chat_args
    )
    memory_name, memory = select_component(
        "memory",
        memory_registry,
        chat_args
    )

    set_conversation_components(
        chat_args.conversation_id, llm_name, retriever_name, memory_name
    )

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=retriever,
        condense_question_llm=ChatOpenAI(streaming=False),
        metadata=chat_args.metadata
    )
