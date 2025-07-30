import os

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import ChatOllama

from memory import get_session_history
from vectorstore import get_vectorstore
from prompts import contextualize_prompt, qa_prompt

def get_rag_chain():     
    # Mude para 'host.docker.internal' para acessar o Ollama no seu hospedeiro
    # A porta deve ser a que o Ollama está usando no seu sistema local (geralmente 11434)
    llm = ChatOllama(model="deepseek-v2:16b", base_url="http://host.docker.internal:11434")
    
    retriever = get_vectorstore().as_retriever()
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_prompt)
    Youtube_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=qa_prompt,
    )
    return create_retrieval_chain(history_aware_retriever, Youtube_chain)

def get_conversational_rag_chain():
    rag_chain = get_rag_chain()
    return RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=get_session_history,
        input_messages_key='input',
        history_messages_key='chat_history',
        output_messages_key='answer',
    )