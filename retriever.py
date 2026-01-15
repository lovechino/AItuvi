from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from functools import lru_cache

VECTOR_PATH = "vector_store/tuvi_bacphai"
EMBED_MODEL = "llama3.2:1b"

# 1️⃣ Load embeddings 1 lần
_embeddings = OllamaEmbeddings(
    model=EMBED_MODEL,
    base_url="http://localhost:11434"
)

# 2️⃣ Load FAISS 1 lần
_faiss_db = FAISS.load_local(
    VECTOR_PATH,
     embeddings=None,
    allow_dangerous_deserialization=True
)

# 3️⃣ Cache retriever
@lru_cache(maxsize=1)
def get_retriever(k: int = 3):
    return _faiss_db.as_retriever(
        search_kwargs={"k": k}
    )
