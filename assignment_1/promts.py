from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.prompts.base import ChatPromptTemplate

# text qa prompt
CUSTOM_TEXT_QA_SYSTEM_PROMPT = ChatMessage(
    content=(
        "You are an expert Q&A system that is trusted around the world.\n"
        "Always answer the query using the provided context information, "
        "and not prior knowledge.\n"
        "Some rules to follow:\n"
        "1. Never directly reference the given context in your answer.\n"
        "2. Avoid statements like 'Based on the context, ...' or "
        "'The context information ...' or anything along those lines."
        "3. Give the URL (include title) of the source where you found the answer.\n"
        "4. Give detail much as possible."
    ),
    role=MessageRole.SYSTEM,
)

CUSTOM_TEXT_QA_PROMPT_TMPL_MSGS = [
    CUSTOM_TEXT_QA_SYSTEM_PROMPT,
    ChatMessage(
        content=(
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "answer the query.\n"
            "Query: {query_str}\n"
            "Answer: "
        ),
        role=MessageRole.USER,
    ),
]

CUSTOM_CHAT_TEXT_QA_PROMPT = ChatPromptTemplate(
    message_templates=CUSTOM_TEXT_QA_PROMPT_TMPL_MSGS
)

# Tree Summarize
CUSTOM_TREE_SUMMARIZE_PROMPT_TMPL_MSGS = [
    CUSTOM_TEXT_QA_SYSTEM_PROMPT,
    ChatMessage(
        content=(
            "Context information from multiple sources is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the information from multiple sources and not prior knowledge, "
            "answer the query.\n"
            "Query: {query_str}\n"
            "Answer: "
        ),
        role=MessageRole.USER,
    ),
]

CUSTOM_CHAT_TREE_SUMMARIZE_PROMPT = ChatPromptTemplate(
    message_templates=CUSTOM_TREE_SUMMARIZE_PROMPT_TMPL_MSGS
)
