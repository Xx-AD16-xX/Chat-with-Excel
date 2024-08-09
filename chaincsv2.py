from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Chat with PDF",
            message="Uplaod pdf and chat with it",
            ),
        cl.Starter(
            label="Chat with Excel/CSV",
            message="Uplaod Excel or csv and chat with it",
            ),
        cl.Starter(
            label="Chat with me",
            message="Hello! How may I help you?",
            )
        ]

@cl.on_chat_start
async def on_chat_start():
    image = cl.Image(path="C:\\Users\\Guest_User\\Desktop\\MAIN\\pdfphoto.jpg", name="cat image", display="side")

    await cl.Message(
        # Notice that the name of the image is referenced in the message content
        content="Here is the cat image!",
        elements=[image],
    ).send()
    
    model = ChatGroq(model="gemma2-9b-it", api_key="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")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very knowledgeable AI Assistance who can answer any question in the world",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)



@cl.on_message
    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
