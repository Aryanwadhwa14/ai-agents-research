import os
import json
import csv

def run_all_evals():
    try:
        from evaluation.rag_eval import run_eval as run_rag
        from evaluation.langchain_eval import run_eval as run_langchain
        from evaluation.llamaindex_eval import run_eval as run_llama
        from evaluation.react_eval import run_eval as run_react
        from evaluation.memgpt_eval import run_eval as run_memgpt
        from evaluation.hiagent_eval import run_eval as run_hiagent
        from evaluation.amem_eval import run_eval as run_amem
        from evaluation.mcp_eval import run_eval as run_mcp
        
        run_rag()
        run_langchain()
        run_llama()
        run_react()
        run_memgpt()
        run_hiagent()
        run_amem()
        run_mcp()
    except Exception as e:
        print(f"Error running sub-evals: {e}")

def compile_results():
    run_all_evals()
    
    architectures = ["RAG", "LangChain", "LlamaIndex", "ReAct", "MemGPT", "HiAgent", "A-MEM", "MCP"]
    all_data = {}
    
    for arch in architectures:
        filename = f"results/{arch}_metrics.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                all_data[arch] = json.load(f)
                
    # Compile latency_metrics.csv
    with open("results/latency_metrics.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Architecture", "Latency_p95_sec"])
        for arch in architectures:
            if arch in all_data:
                writer.writerow([arch, all_data[arch]["latency_p95_sec"]])

    # Compile tokens_usage.json
    tokens = {arch: all_data[arch]["token_usage"] for arch in architectures if arch in all_data}
    with open("results/tokens_usage.json", "w") as f:
        json.dump(tokens, f, indent=2)

    # Compile evaluation_scores.md
    with open("results/evaluation_scores.md", "w") as f:
        f.write("# Memory Architectures Benchmark Scores\n\n")
        f.write("| Architecture | Single-Hop Acc | Multi-Hop Acc | Adaptability |\n")
        f.write("|--------------|----------------|----------------|--------------|\n")
        for arch in architectures:
            if arch in all_data:
                d = all_data[arch]
                f.write(f"| {arch} | {d['single_hop_accuracy']}% | {d['multi_hop_accuracy']}% | {d['adaptability']} |\n")

    print("Evaluations completed. Metrics aggregated successfully in `/results/`.")

if __name__ == "__main__":
    compile_results()
