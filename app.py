from fastapi import FastAPI, Request
from evolution_api import send_whatsapp_message
from bot.ai_bot import AIBot
# from message_buffer import buffer_message

app = FastAPI()
ai_bot = AIBot()

@app.post('/webhook')
async def webhook(request: Request):
    data = await request.json()
    chat_id = data.get('data').get('key').get('remoteJid')
    message = data.get('data').get('message').get('conversation')

    if chat_id and message and not '@g.us' in chat_id:
        # await buffer_message(
        #     chat_id=chat_id,
        #     message=message,
        # )
        response = ai_bot.invoke(question=message)
        send_whatsapp_message(
            number=chat_id,
            text=response,
        )

    return {'status': 'ok'}
