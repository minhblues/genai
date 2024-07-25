# Assignment_1 AI BOT

This is a simple AI bot that can answer some questions from source https://www.llamaindex.ai/blog

## Installation

```bash
pip install -r requirements.txt
```
## Config
Update `openai_key` in config.py  
Update `reindex` when craw new blogs in config.py
```python
"llm": llm,
"reindex": False,
"openapi_key": openapi_key,
```

## Run
```bash
python3 main.py
```

## Questions

```markdown
1. Enter your question (press Ctrl+D to exit): What are key features of llama-agents?

Response:
The key features of llama-agents include:

1. **Distributed Service Oriented Architecture:** Each agent can operate as an independent microservice, managed by a customizable LLM-powered control plane that handles task routing and distribution.
2. **Communication via standardized API interfaces:** Agents communicate through a central control plane orchestrator, using a message queue to pass messages between them.
3. **Define agentic and explicit orchestration flows:** Developers can either directly define the sequence of interactions between agents or use an “agentic orchestrator” to determine the relevant agents for a task.
4. **Ease of deployment:** The framework allows for the independent launch, scaling, and monitoring of each agent and the control plane.
5. **Scalability and resource management:** Built-in observability tools help monitor the quality and performance of the system and each individual agent service.

For more details, visit [Introducing llama-agents: A Powerful Framework for Building Production Multi-Agent AI Systems — LlamaIndex, Data Framework for LLM Applications](https://www.llamaindex.ai/blog/introducing-llama-agents-a-powerful-framework-for-building-production-multi-agent-ai-systems).
```

```markdown
2. Enter your question (press Ctrl+D to exit): What are the two critical areas of RAG system performance that are assessed in the "Evaluating RAG with LlamaIndex" section of the OpenAI Cookbook?

Response: 
The two critical areas of RAG system performance assessed in the "Evaluating RAG with LlamaIndex" section of the OpenAI Cookbook are the Retrieval System and Response Generation.

For more details, you can visit the source: [OpenAI Cookbook: Evaluating RAG systems — LlamaIndex, Data Framework for LLM Applications](https://www.llamaindex.ai/blog/openai-cookbook-evaluating-rag-systems-fe393c61fb93).
```

```markdown
3. Enter your question (press Ctrl+D to exit): What are the two main metrics used to evaluate the performance of the different rerankers in the RAG system?

Response: 
The two main metrics used to evaluate the performance of the different rerankers in the RAG system are **Hit Rate** and **Mean Reciprocal Rank (MRR)**.

For more details, you can visit the source: [Boosting RAG: Picking the Best Embedding & Reranker models — LlamaIndex, Data Framework for LLM Applications](https://www.llamaindex.ai/blog/boosting-rag-picking-the-best-embedding-reranker-models-42d079022e83).
```
