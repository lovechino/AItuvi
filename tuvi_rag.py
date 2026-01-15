import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM

from retriever import get_retriever
from llm.prompt import SYSTEM_PROMPT, USER_PROMPT
# from llm.ollama import llm
# =========================
# 1️⃣ Load GLOBAL (1 lần)
# =========================
llm = OllamaLLM(
    model="llama3.2:1b",
    temperature=0.2,
    keep_alive="5m"
)


retriever = get_retriever(k=3)

prompt = PromptTemplate(
    input_variables=["context", "chart", "year"],
    template=SYSTEM_PROMPT + "\n" + USER_PROMPT
)

chain = prompt | llm | StrOutputParser()

# =========================
# 2️⃣ Preload context (QUAN TRỌNG)
# =========================

STATIC_QUERY = (
    "Tử Vi Đẩu Số Bắc phái, tam hợp, giáp cung, "
    "tứ hóa, luận hạn, đại vận, tiểu vận"
)

def json_parser(output: str):
    try:
        return json.loads(output)
    except Exception:
        return {
            "error": "Invalid JSON from model",
            "raw": output
        }

# STATIC_CONTEXT = retriever.invoke(STATIC_QUERY)

# =========================
# 3️⃣ Function runtime (NHẸ)
# =========================

def analyze_tuvi(chart_result: dict, year: int) -> str:
    raw = chain.invoke({
        "context": STATIC_QUERY,
        "chart": json.dumps(chart_result, ensure_ascii=False, indent=2),
        "year": year
    })
    return json_parser(raw)
