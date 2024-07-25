llm = "openai"
openapi_key = ""


def load_config():
    return {
        "llm": llm,
        "reindex": True,
        "openapi_key": openapi_key,
    }
