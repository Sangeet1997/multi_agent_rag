from langchain_ollama import OllamaLLM

def query_ollama(prompt):

    llm = OllamaLLM(model="llama3.2")
    result = llm.invoke(prompt)
    return result