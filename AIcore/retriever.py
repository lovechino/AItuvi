from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

VECTOR_PATH = "vector_store/tuvi_bacphai"
EMBED_MODEL = "llama3.2:1b"

def load_retriever(k=5):
    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url="http://localhost:11434"
    )

    db = FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db.as_retriever(
        search_kwargs={"k": k}
    )
