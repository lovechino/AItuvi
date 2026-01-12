import subprocess
from langchain_ollama import OllamaLLM


model="llama3.2:1b"
def get_llm():
    return OllamaLLM(
        model=model,
        temperature=0.2,
        base_url="http://localhost:11434"
    )


