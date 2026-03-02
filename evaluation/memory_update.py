import os
import json
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
import time

# Initial memory setup
initial_facts = [
    Document(page_content="The user's favorite color is blue."),
    Document(page_content="The user's favorite food is sushi.")
]

updated_facts = [
    Document(page_content="The user's favorite color is green."),  # Overwrites old color
    Document(page_content="The user's favorite food is ramen.")    # Overwrites old food
]

embedding_model = OpenAIEmbeddings()
llm = ChatOpenAI(temperature=0)

# Step 1: Index initial memory
db_initial = FAISS.from_documents(initial_facts, embedding_model)
retriever_initial = db_initial.as_retriever()
qa_initial = RetrievalQA.from_chain_type(llm=llm, retriever=retriever_initial)

# Query initial state
query = "What is the user's favorite color?"
start_1 = time.time()
initial_answer = qa_initial.run(query)
time_1 = time.time() - start_1

# Step 2: Update memory (simulate overwrite)
db_updated = FAISS.from_documents(updated_facts, embedding_model)
retriever_updated = db_updated.as_retriever()
qa_updated = RetrievalQA.from_chain_type(llm=llm, retriever=retriever_updated)

start_2 = time.time()
updated_answer = qa_updated.run(query)
time_2 = time.time() - start_2

# Save results
os.makedirs("results", exist_ok=True)
results = {
    "query": query,
    "initial_answer": initial_answer,
    "initial_latency_sec": round(time_1, 2),
    "updated_answer": updated_answer,
    "updated_latency_sec": round(time_2, 2)
}

with open("results/memory_update_test.json", "w") as f:
    json.dump(results, f, indent=2)

print("Memory update test completed. Results saved to results/memory_update_test.json")
