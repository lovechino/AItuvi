import json
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from retriever import load_retriever
from llm.prompt import SYSTEM_PROMPT, USER_PROMPT

llm = OllamaLLM(model="llama3.2:1b")



def analyze_tuvi(chart_result: dict, year: int):
    retriever = load_retriever(k=5)
    prompt = PromptTemplate(
        input_variables=["context", "chart", "year"],
        template=SYSTEM_PROMPT + "\n" + USER_PROMPT
    )

    chain = (
        {
            # ✅ retriever chỉ nhận STRING
            "context": lambda _: retriever.invoke(
                "Tử Vi Đẩu Số Bắc phái, tam hợp, giáp cung, tứ hóa, luận hạn"
            ),

            # ✅ dữ liệu người dùng giữ nguyên
            "chart": lambda x: x["chart"],
            "year": lambda x: x["year"]
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "chart": json.dumps(chart_result, ensure_ascii=False, indent=2),
        "year": year
    })
