import os

# Remova a importação de decouple e GROQ_API_KEY se não forem mais usados em outro lugar
# from decouple import config
# from config import GROQ_API_KEY

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
# Importe ChatOllama em vez de ChatGroq
from langchain_community.chat_models import ChatOllama


class AIBot:

    def __init__(self):
        # Configuração para usar o Ollama local
        # Substitua 'llama2' pelo nome do seu modelo Ollama (ex: 'mistral', 'gemma')
        # E ajuste a URL se sua instância Ollama não estiver na porta 11434 ou em outro host
        self.__chat = ChatOllama(model="deepseek-v2:16b", base_url="http://host.docker.internal:11434")

    def invoke(self, question):
        prompt = PromptTemplate(
            input_variables=['texto'],
            template='''
            Responda as perguntas dos usuários com base no texto abaixo.
            Você é um assistente especializado em tirar dúvidas sobre o caju sendo um representante da empresa cardeal.
            Tire dúvidas dos possíveis alunos que entrarem em contato.
            Responda de forma natural, agradável e respeitosa. Seja objetivo nas respostas, com informações
            claras, suscinta e diretas. Foque em ser natural e humanizado, como um diálogo comum entre duas pessoas.
            Leve em consideração também o histórico de mensagens da conversa com o usuário.
            Responda sempre em português brasileiro.
            <texto>
            {texto}
            </texto>
            '''
        )
        chain = prompt | self.__chat | StrOutputParser()
        response = chain.invoke({
            'texto': question,
        })
        return response