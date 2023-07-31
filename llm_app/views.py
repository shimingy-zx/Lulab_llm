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
        raw_documents = TextLoader('static/demo.txt', 'utf-8').load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)
        db = Chroma.from_documents(documents, OpenAIEmbeddings())

        query = request.POST.get('q')
        # docs = db.similarity_search(query)

        embedding_vector = OpenAIEmbeddings().embed_query(query)
        docs = db.similarity_search_by_vector(embedding_vector)

        # print(docs[0])
        #
        # poe = docs[0].page_content

        return Response({"content": docs[0].page_content})
