import os
from telethon import TelegramClient, events
import asyncio
import httpx

# Replace with your actual API ID, API hash, and bot token
API_ID = 1234567
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'
GROQ_API_KEY = 'your_groq_api_key'

client = TelegramClient('session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def get_groq_response(prompt):
    async with httpx.AsyncClient() as groq_client:
        response = await groq_client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 100
            },
            timeout=60
        )
        return response.json()['choices'][0]['message']['content']

@client.on(events.NewMessage)
async def echo(event):
    try:
        response_text = await get_groq_response(event.message.message)
        await event.respond(response_text)
    except Exception as e:
        await event.respond(f"Error processing message: {str(e)}")

async def main():
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())