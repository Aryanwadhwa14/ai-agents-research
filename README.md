# Memory Framework Orchestrator: Addressing Memory Limitations in LLM-Based Agents

This repository contains the implementation of a modular memory evaluation framework designed to benchmark and reproduce the results discussed in the research paper **"Addressing Memory Limitations in LLM-Based Agents"**. It automates the evaluation of various memory solutions like Retrieval-Augmented Generation (RAG), agent state updates, and multi-session memory recall.

## What Has Been Accomplished So Far

With respect to the research paper, the following systems and evaluations have been implemented:

### 1. Memory Architectures and Pipelines
- **LangChain & FAISS Integration (`/frameworks/langchain_pipeline.py`)**: A scalable pipeline that ingests long context, manages document chunking, and vectors them into a FAISS local vector database, serving as the foundational RAG implementation evaluated in the paper.
- **Utility Components (`/utils`)**: 
  - `chunking.py`: Systematic document chunking allowing empirical comparisons of chunk sizes (256, 512, 1024), mapping to the paper's context limit studies. 
  - `timer.py`: A latency tracker to record time metrics for vector indexing and answering.
  - `judge.py`: An LLM-as-a-judge scorer that evaluates whether the retrieved memory successfully matched the original context fact, facilitating automated accuracy scoring.

### 2. Paper Evaluation Protocols
We have successfully set up three core evaluation scripts corresponding to the core memory limitations discussed in the research:
- **RAG Chunking Benchmark (`evaluation/rag_chunk_benchmark.py`)**: Tests context window latency and generation precision against variable document chunk sizes to evaluate computational tradeoffs.
- **Dynamic Memory Updates (`evaluation/agent_update_eval.py`)**: Tests agent capability to seamlessly drop old memory facts (e.g., favorite color is blue) and prioritize updated episodic memories (e.g., favorite color is green) directly addressing the overwrite conflict problems in LLMs.
- **Cross-Session Retrieval (`evaluation/multi_session_recall.py`)**: Benchmarks how effectively an agent recalls context built progressively over multiple independent conversations.

### 3. Automated Orchestration
- **Main Evaluator (`evaluation/main_runner.py`)**: Serves as the primary entry point to benchmark all test configurations locally. It handles running the independent evaluation modules recursively and includes robust fallback structures to execute natively without requiring active network API endpoints.

## Project Structure

```
├── README.md                      # This file
├── evaluation/                    # Core evaluation scripts for benchmarking
│   ├── main_runner.py             # Benchmarking entry point
│   ├── rag_chunk_benchmark.py     # RAG Latency vs Chunk Size
│   ├── agent_update_eval.py       # Memory Overwrite accuracy
│   └── multi_session_recall.py    # Cross-conversation recall
├── frameworks/
│   └── langchain_pipeline.py      # Vector DB routing & FAISS abstractions
├── utils/
│   ├── chunking.py                # LangChain Recursive character splitters
│   ├── timer.py                   # Generation latency telemetry
│   └── judge.py                   # Automated response grader
├── data/                          # Datasets (e.g. `long_docs/sample.txt`)
└── results/                       # Automated execution output directory
    ├── evaluation_scores.md       # Summarized grades of the agent 
    ├── latency_metrics.csv        # Speed evaluation logs
    └── tokens_usage.json          # Agent token overhead logs
```

## Running the Benchmarks
To run the automated suite and generate local metric charts and evaluation logs:

```bash
pip install -r requirements.txt
python evaluation/main_runner.py
```

Check the `/results` folder for detailed CSV and JSON traces of the agent evaluations.
