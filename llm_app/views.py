from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.vectorstores import Milvus
from django.conf import settings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

import os


class QueryChat(APIView):
    @staticmethod
    def get(request):
        """
        """
        # req = request.query_params.dict()#前端给的json包数据
        # student_name = req["student_name"]

        student_id = {"fjidsoajf"}  # 提取数据表中数据
        return Response(student_id)  # 返回数据，这里由于提取数据表中数据直接就是jason格式所以可以直接传，其他的需要转为json格式

    @staticmethod
    def post(request):
        """
        """

        embeddings = OpenAIEmbeddings()

        milvus_store = Milvus(
            embedding_function=embeddings,
            collection_name="LangChainCollection",
            connection_args={"host": settings.MILVUS_HOST, "port": settings.MILVUS_PORT},
            # drop_old = True,
        )

        query = request.POST.get('q')
        docs = milvus_store.similarity_search(query, 3)

        corpus = docs[0].page_content+docs[1].page_content+docs[2].page_content

        class CommaSeparatedListOutputParser(BaseOutputParser):
            """Parse the output of an LLM call to a comma-separated list."""

            def parse(self, text: str):
                """Parse the output of an LLM call."""
                return text.strip().split(", ")

        template = """你是陆向谦实验室的AI助理，请结合问题和参考语料，回答问题"""

        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = """问题：{text}；参考语料："""+corpus
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(
            llm=ChatOpenAI(),
            prompt=chat_prompt,
            output_parser=CommaSeparatedListOutputParser()
        )
        # chain.run("colors")
        # print(chain.run("陆向谦实验室理念？"))

        return Response({"content":chain.run(query) })


        # 获取文件示例代码
        # raw_documents = TextLoader('static/demo.txt', 'utf-8').load()
        # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        # documents = text_splitter.split_documents(raw_documents)
        # db = Chroma.from_documents(documents, OpenAIEmbeddings())
        #
        # query = request.POST.get('q')
        # # docs = db.similarity_search(query)
        #
        # embedding_vector = OpenAIEmbeddings().embed_query(query)
        # docs = db.similarity_search_by_vector(embedding_vector)

        # return Response({"content": docs[0].page_content})