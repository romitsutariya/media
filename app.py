from openai import AsyncOpenAI
import chainlit as cl
client = AsyncOpenAI()

# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    # ... more settings
}

@cl.on_message
async def on_message(message: cl.Message):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": "You are a helpful bot, write sql schema base on table name provided by user for postgre",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        **settings
    )
    await cl.Message(content=response.choices[0].message.content).send()
