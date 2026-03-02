import os
import json
import time
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools import Tool as LangchainTool

# Simulated agent tools with distinct memory scopes
# Each agent/tool has their own isolated memory chunk
system_docs = ["To reset a Linux password, use the passwd command."]
data_docs = ["Customer churn is highest in Q3."]

embedding_model = OpenAIEmbeddings()
system_db = FAISS.from_texts(system_docs, embedding_model)
data_db = FAISS.from_texts(data_docs, embedding_model)

# Define retrieval tools for each domain
def system_query_tool(query: str) -> str:
    return system_db.similarity_search(query, k=1)[0].page_content

def data_query_tool(query: str) -> str:
    return data_db.similarity_search(query, k=1)[0].page_content

system_tool = LangchainTool(name="SystemTool", func=system_query_tool, description="Handles system-level questions.")
data_tool = LangchainTool(name="DataTool", func=data_query_tool, description="Handles customer data questions.")

# Initialize multi-tool agent
llm = ChatOpenAI(temperature=0)
agent = initialize_agent(
    tools=[system_tool, data_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Simulate routing behavior across agents
query_1 = "How do I reset a user password on Linux?"
query_2 = "When does customer churn peak?"

start = time.time()
response_1 = agent.run(query_1)
response_2 = agent.run(query_2)
latency = round(time.time() - start, 2)

# Save results
os.makedirs("results", exist_ok=True)
with open("results/mcp_agent_routing.json", "w") as f:
    json.dump({
        "query_1": query_1,
        "response_1": response_1,
        "query_2": query_2,
        "response_2": response_2,
        "total_latency_sec": latency
    }, f, indent=2)

print("MCP-style agent routing test completed. Results saved to results/mcp_agent_routing.json")
