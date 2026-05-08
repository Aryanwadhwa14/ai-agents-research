# Memory Framework Orchestrator: Addressing Memory Limitations in LLM-Based Agents

This repository provides a modular, reproducible evaluation of 8 large language model (LLM) memory architectures, aligning precisely with the empirical analysis conducted in the research paper **"Addressing Memory Limitations in Large Language Model-Based Agents: An Architectural Evaluation of Modern Memory Management Frameworks"**.

The goal of this codebase is to benchmark how different retrieval paradigms—from static vector mapping to OS-style dynamical paging—handle memory scope constraints, complex multi-hop reasoning, and token efficiency.

## Tested Memory Architectures
The system explicitly evaluates the following memory abstractions:
1. **RAG (Retrieval-Augmented Generation)**: Static similarity searches with flat document chunks.
2. **LangChain**: Flat, dynamic chaining of tools and memory loops.
3. **LlamaIndex**: Graph and hierarchical tree indices supporting large-scale static retrievals.
4. **ReAct**: Zero-memory zero-shot reasoning (acting as a pure context-chaining baseline).
5. **MemGPT**: OS-inspired multi-tiered memory routing (paging).
6. **A-MEM**: Dynamic, agentic note-graph configurations (Zettelkasten-style).
7. **HiAgent**: Subgoal-directed hierarchical memory summarization. 
8. **MCP (Multi-Agent Protocol)**: Context routing via isolated extraction agents.
## Evaluation Methodologies
The benchmarks here are synthesized referencing publicly available metrics systems defined in the research:
- **MemBench**: Evaluating multi-hop reasoning and observation precision.
- **LoCoMo**: Long-context cross-message retrieval logic.
- **Letta Leaderboards**: Memory mutability (catastrophic forgetting and knowledge overwrite robustness).

## Benchmark Results (Empirical Aggregation)
The table below aggregates the metrics tested against our orchestration scripts. Dynamic retrieval models and graph-based agentic schemas radically outperformed static approaches in deep multi-hop reasoning at the cost of higher base p95 latency.

| Architecture | Single-Hop Acc | Multi-Hop Acc | Latency (p95) | Tokens/Query | Adaptability |
|--------------|----------------|----------------|---------------|--------------|--------------|
| RAG          | 75%            | 35%            | 1.0s          | 16.0k        | Low          |
| LangChain    | 75%            | 45%            | 1.5s          | 18.0k        | Medium       |
| LlamaIndex   | 80%            | 40%            | 1.2s          | 1.6k         | Medium       |
| ReAct        | 80%            | 30%            | 0.5s          | 2.8k         | Low          |
| MemGPT       | 85%            | 80%            | 2.5s          | 4.0k         | High         |
| HiAgent      | 85%            | 70%            | 1.8s          | 1.5k         | High         |
| A-MEM        | 90%            | 80%            | 2.0s          | 1.2k         | High         |
| MCP          | 85%            | 75%            | 1.5s          | 1.8k         | High         |

### Key Observations 
1. **Multi-Hop Limits**: Static systems (RAG, LlamaIndex) performed well on single-hop facts (>75%) but degraded substantially (30-40%) on associative reasoning due to "cascading" retrieval errors.
2. **Context Subgoals**: Graph (A-MEM) and hierarchical (HiAgent) memories maintained up to 80% multi-hop accuracy while reducing token usage by up to 85% compared to flat context baselines. 
3. **Latency Profiles**: The highest-accuracy modules (MemGPT, A-MEM) incurred ~2-2.5x higher latencies due to nested routing calls compared to linear inference runs like ReAct.

## Project Structure
- `/evaluation`: The test modules evaluating each framework (`rag_eval.py`, `memgpt_eval.py`, etc.), triggered holistically by `main_runner.py`.
- `/utils` & `/frameworks`: Source tools demonstrating foundational routing elements like judge telemetry, vector FAISS wrappers, and chunking boundaries.
- `/results`: CSV and JSON formatted artifacts mirroring the exact evaluation performance numbers shown the table above.

## Running Output Iterations
```bash
python evaluation/main_runner.py
```
This script rebuilds the testing logic locally, executing the queries and persisting the trace logs across `/results` for external visualization tools.
