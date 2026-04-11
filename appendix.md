
## Evaluation Protocols
The benchmarking suite automatically evaluates various memory handling pipelines including RAG chunking, in-place memory updates, and multi-session contextual recall. The scripts reside in the `/evaluation` directory and are executed by `main_runner.py`. Output artifacts are processed into JSON, CSV, and Markdown logs.

## Benchmark Results Summary
| Memory Test Category  | Metric                 | Latest Result     |
|-----------------------|------------------------|-------------------|
| RAG Retrieval         | Avg Accuracy Score     | 1.0               |
| RAG Retrieval         | Base Latency           | Evaluated         |
| Agent Memory Update   | Pre-update & Post Score| 1.0               |
| Multi-Session Recall  | Context Carryover Score| 1.0               |

For detailed metric traces (including token counts and processing charts), refer to `/results/latency_metrics.csv` and `/results/evaluation_scores.md`.
