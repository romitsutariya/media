import chainlit as cl
import getpass
import os

import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@cl.on_chat_start
async def start():
    files = None
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    loader = PyPDFLoader("./input_doc/input.pdf")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(),persist_directory="./data")
    prompt = hub.pull("rlm/rag-prompt")
    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    cl.user_session.set("llm_chain", rag_chain)

@cl.on_message
async def query_llm(message: cl.Message):
    rag_chain = cl.user_session.get("llm_chain")
    msg = cl.Message(content="")
    for chunk in rag_chain.stream(message.content):
              await  msg.stream_token(chunk)
    await msg.update()