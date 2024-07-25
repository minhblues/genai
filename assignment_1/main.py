import json
import os

import openai
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

from promts import CUSTOM_CHAT_TEXT_QA_PROMPT, CUSTOM_CHAT_TREE_SUMMARIZE_PROMPT
from helper import retry_with_exponential_backoff
from web_crawling import craw_blogs
from config import load_config

config = load_config()

if config["llm"] == "openai":
    openai.api_key = config["openapi_key"]
    Settings.llm = OpenAI(model="gpt-4o")
    Settings.embed_model = OpenAIEmbedding(
        model_type=OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE
    )

print("LLM model loaded")

if config["reindex"]:
    craw_blogs()

PERSIST_DIR = "./database"
print(f"Checking if storage existed at {PERSIST_DIR}", end=" ")
if not os.path.exists(PERSIST_DIR):
    print("- not found, will be create index in next step")
    config["reindex"] = True
else:
    print("- found")
    config["reindex"] = False

if config["reindex"]:
    # Normalizing the data
    reader = SimpleDirectoryReader(input_dir="./blogs", required_exts=[".json"])
    all_docs = []
    for docs in reader.iter_data():
        for doc in docs:
            json_doc = json.loads(doc.text)
            doc.metadata = {
                "document_title": json_doc["title"],
                "document_date": json_doc["date"],
                "document_url": json_doc["link"],
            }
            doc.text = json_doc["content"]
            all_docs.append(doc)

    print(f"Total number of documents: {len(all_docs)}")

    parser = SentenceSplitter()
    nodes = parser.get_nodes_from_documents(all_docs)
    print(f"Total number of nodes: {len(nodes)}")

    summary_index = SummaryIndex(nodes, show_progress=True)
    vector_index = VectorStoreIndex(nodes, show_progress=True)

    print("Indexes created, saving to disk", end=" ")
    summary_index.storage_context.persist(persist_dir=PERSIST_DIR + "/summary_index")
    vector_index.storage_context.persist(persist_dir=PERSIST_DIR + "/vector_index")
    print(" - done")

else:
    # load indexs from disk
    print("Loading indexes from disk", end=" ")
    summary_storage_context = StorageContext.from_defaults(
        persist_dir=PERSIST_DIR + "/summary_index"
    )
    summary_index = load_index_from_storage(summary_storage_context)
    vector_storage_context = StorageContext.from_defaults(
        persist_dir=PERSIST_DIR + "/vector_index"
    )
    vector_index = load_index_from_storage(vector_storage_context)
    print(" - done")

# Query Engine
summary_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize",
    use_async=True,
    tree_summarize_template=CUSTOM_CHAT_TREE_SUMMARIZE_PROMPT,
)
vector_query_engine = vector_index.as_query_engine(
    text_qa_template=CUSTOM_CHAT_TEXT_QA_PROMPT
)

summary_tool = QueryEngineTool.from_defaults(
    query_engine=summary_query_engine,
    description="Useful for summarization questions related to any topic in all the blogs",
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="Useful for retrieving specific context from the blogs",
)

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[summary_tool, vector_tool],
    verbose=True,
)


@retry_with_exponential_backoff
def ask_question(**kwargs):
    return query_engine.query(**kwargs)


# Ask question
if __name__ == "__main__":
    try:
        while True:
            line = input("Enter your question (press Ctrl+D to exit): ")
            response = ask_question(str_or_query_bundle=line)
            print("Response: ")
            print(response)
            print("-" * 20)
    except EOFError:
        print(
            "There's some issue with the input, or maybe your API key hit the rate limit. Exiting..."
        )
        pass
