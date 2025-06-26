
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from config import (
    GROQ_API_KEY
)

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory

from memory import get_session_history
from vectorstore import get_vectorstore
from prompts import contextualize_prompt, qa_prompt

class AIBot:

    def __init__(self):
        self.__chat = ChatGroq(model='llama-3.3-70b-versatile')

    def invoke(self, question):
        llm = ChatGroq(model='llama-3.3-70b-versatile')
        retriever = get_vectorstore().as_retriever()
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_prompt)
        question_answer_chain = create_stuff_documents_chain(
            llm=llm,
            prompt=qa_prompt,
        )
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        return RunnableWithMessageHistory(
            runnable=rag_chain,
            get_session_history=get_session_history,
            input_messages_key='input',
            history_messages_key='chat_history',
            output_messages_key='answer',
        )
