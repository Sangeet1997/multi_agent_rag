from langchain_ollama import OllamaLLM
import chromadb
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os


def query_groq(prompt):
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
    )
    result = llm.invoke(prompt)
    print(result)
    return result.content



def query_ollama(prompt):

    llm = OllamaLLM(model="llama3.2")
    result = llm.invoke(prompt)
    return result

def query_rag(query_text, n_results=3):

    chroma_client = chromadb.Client()
    
    try:
        collection = chroma_client.get_collection(name="basic_rag")
    except:  # Collection doesn't exist
        return "No documents have been uploaded yet. Please upload a PDF first."
    
    # Query collection for relevant documents
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Combine retrieved documents
    context = "\n\n".join(results['documents'][0])
    
    # Create prompt template
    prompt_template = PromptTemplate.from_template("""
    Answer the question based on the following context. If the answer cannot be found 
    in the context, say "I cannot find the answer in the provided context."

    Context: {context}

    Question: {question}

    Answer: """)
    
    # Format prompt with context and query
    prompt = prompt_template.format(context=context, question=query_text)
    
    # Query Ollama
    llm = OllamaLLM(model="llama3.2")  
    result = llm.invoke(prompt)
    
    return result