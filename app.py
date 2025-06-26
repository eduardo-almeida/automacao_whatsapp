from fastapi import FastAPI, Request
from evolution_api import send_whatsapp_message
from bot.ai_bot import AIBot
from chains import get_conversational_rag_chain
# from message_buffer import buffer_message

app = FastAPI()
ai_bot = AIBot()
# conversational_rag_chain = get_conversational_rag_chain()

@app.post('/webhook')
async def webhook(request: Request):
    data = await request.json()
    chat_id = data.get('data').get('key').get('remoteJid')
    message = data.get('data').get('message').get('conversation')

    if chat_id and message and not '@g.us' in chat_id:
        response = ai_bot.invoke(question=message)
        # response = conversational_rag_chain.invoke(
        #     input= {'input': message},
        #     config= {'configuration': {'session_id': chat_id,}},
        # )['answer']

        send_whatsapp_message(
            number=chat_id,
            text=response,
        )

    return {'status': 'ok'}
