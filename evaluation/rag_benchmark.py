import os
import time
import json
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Load a long document (you can replace this with a larger file)
loader = TextLoader("data/long_docs/sample.txt")
documents = loader.load()

# Define chunk sizes to test
chunk_sizes = [256, 512, 1024]
embedding_model = OpenAIEmbeddings()
llm = ChatOpenAI(temperature=0)

results = {}

for size in chunk_sizes:
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    # Index and build retriever
    db = FAISS.from_documents(chunks, embedding_model)
    retriever = db.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    query = "What is the main idea of the second section?"
    start_time = time.time()
    answer = qa_chain.run(query)
    latency = time.time() - start_time

    results[size] = {
        "chunk_count": len(chunks),
        "latency_sec": round(latency, 2),
        "answer": answer
    }

# Save benchmark results
os.makedirs("results", exist_ok=True)
with open("results/rag_chunk_benchmark.json", "w") as f:
    json.dump(results, f, indent=2)

print("Benchmark completed. Results saved to results/rag_chunk_benchmark.json")
