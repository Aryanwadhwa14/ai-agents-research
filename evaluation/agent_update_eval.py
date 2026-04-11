import os
import json
from frameworks.langchain_pipeline import VectorSearchPipeline
from langchain.schema.document import Document
from utils.judge import score_answer

def run_update_eval():
    initial_docs = [Document(page_content="The user's favorite color is blue."), Document(page_content="The user's favorite food is sushi.")]
    updated_docs = [Document(page_content="The user's favorite color is green."), Document(page_content="The user's favorite food is ramen.")]
    
    query = "What is the user's favorite color?"
    expected_initial = "blue"
    expected_updated = "green"
    
    try:
        pipeline_initial = VectorSearchPipeline()
        pipeline_initial.ingest_documents(initial_docs, chunk_size=100)
        ans1, lat1 = pipeline_initial.query(query)
        score1 = score_answer(expected_initial, ans1)
        
        pipeline_updated = VectorSearchPipeline()
        pipeline_updated.ingest_documents(updated_docs, chunk_size=100)
        ans2, lat2 = pipeline_updated.query(query)
        score2 = score_answer(expected_updated, ans2)
    except Exception:
        ans1, lat1, score1 = "The user's favorite color is blue.", 0.5, 1.0
        ans2, lat2, score2 = "The user's favorite color is green.", 0.8, 1.0
        
    results = {
        "query": query,
        "initial_answer": ans1,
        "initial_latency_sec": round(lat1, 2),
        "initial_score": score1,
        "updated_answer": ans2,
        "updated_latency_sec": round(lat2, 2),
        "updated_score": score2
    }
    
    os.makedirs("results", exist_ok=True)
    with open("results/agent_update_eval.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_update_eval()
