from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from utils.chunking import create_chunks
from utils.timer import get_latency
from typing import List
from langchain.schema.document import Document

class VectorSearchPipeline:
    def __init__(self, embedding_model=None, llm=None):
        self.embedding_model = embedding_model or OpenAIEmbeddings()
        self.llm = llm or ChatOpenAI(temperature=0)
        self.db = None
        self.qa_chain = None

    def ingest_documents(self, documents: List[Document], chunk_size=512):
        chunks = create_chunks(documents, chunk_size=chunk_size)
        self.db = FAISS.from_documents(chunks, self.embedding_model)
        retriever = self.db.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=retriever)
        return len(chunks)

    def query(self, question: str):
        if not self.qa_chain:
            raise ValueError("No documents ingested yet.")
        answer, latency = get_latency(self.qa_chain.run, question)
        return answer, latency
