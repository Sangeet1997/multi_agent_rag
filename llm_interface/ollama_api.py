from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def query_ollama(prompt):
    ollama = Ollama(base_url="http://localhost:11400")
    
    template = "{prompt}"
    prompt_template = PromptTemplate(template=template, input_variables=["prompt"])
    
    chain = LLMChain(llm=ollama, prompt=prompt_template)
    
    response = chain.run(prompt)
    return response
