import os
import pdfplumber
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document as LC_Document

DATA_DIR = "data"
VECTOR_DIR = "vector_store"


EMBED_MODEL = "llama3.2:1b"



def load_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap

    return chunks


def convert():
    os.makedirs(VECTOR_DIR, exist_ok=True)

    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url="http://localhost:11434"
    )

    documents = []

    for file in os.listdir(DATA_DIR):
        if not file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(DATA_DIR, file)
        print(f"📄 Đang xử lý: {file}")

        text = load_pdf(pdf_path)
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            documents.append(
                LC_Document(
                    page_content=chunk,
                    metadata={
                        "source": file,
                        "chunk_id": i
                    }
                )
            )

    print(f"📚 Tổng số chunk: {len(documents)}")
    
    # if not documents:
    #     raise ValueError("❌ Không có document nào để embed")
    print("loading 1")
    db = FAISS.from_documents(documents, embeddings)
    # print(db)
    print("loading 2")
    save_path = os.path.join(VECTOR_DIR, "tuvi_bacphai")
    print("loading 3")
    print(save_path)
    print("loading 4")
    db.save_local(save_path)
    print("loading 5")

    # print(f"✅ Vector DB đã lưu tại: {save_path}")


if __name__ == "__main__":
    convert()
