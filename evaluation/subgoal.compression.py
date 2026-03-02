import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Simulated multi-step task log
task_steps = [
    "User logged into the system.",
    "Checked for recent error logs.",
    "Restarted the authentication service.",
    "Confirmed resolution of issue via logs.",
    "Notified admin of successful fix."
]

# Create long context from steps
raw_context = "\n".join(task_steps)
doc = Document(page_content=raw_context)

# Load LLM summarization chain
llm = ChatOpenAI(temperature=0)
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")

# Summarize subgoal actions into compressed memory
summary = summary_chain.run([doc])

# Save result
os.makedirs("results", exist_ok=True)
with open("results/subgoal_compression.json", "w") as f:
    json.dump({
        "raw_steps": task_steps,
        "summary": summary
    }, f, indent=2)

print("Subgoal summarization completed. Result saved to results/subgoal_compression.json")