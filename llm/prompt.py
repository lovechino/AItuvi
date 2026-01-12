import subprocess
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2:1b")

SYSTEM_PROMPT = """
Bạn là chuyên gia Tử Vi Đẩu Số Bắc phái.
Luận đoán dựa trên:
- 14 chính tinh
- Miếu / Vượng / Đắc
- Tứ Hóa
- Đại vận – Tiểu vận – Lưu niên
- Tam hợp – xung chiếu – giáp cung

Quy tắc:
- KHÔNG mê tín
- KHÔNG phán định tuyệt đối
- Luận theo logic học thuật
Dữ liệu lá số Tử Vi (JSON):
{chart_json}
Yêu cầu:
1. Luận tổng quan cuộc đời
2. Luận sự nghiệp – tài chính
3. Luận tình cảm – hôn nhân
4. Luận năm {nam_xem}
5. Chỉ ra cung mạnh – cung yếu
"""

def ask_llm(chart_json,nam_xem):
    SYSTEM_PROMPT = """
        Bạn là chuyên gia Tử Vi Đẩu Số Bắc phái.
        Luận đoán dựa trên:
        - 14 chính tinh
        - Miếu / Vượng / Đắc
        - Tứ Hóa
        - Đại vận – Tiểu vận – Lưu niên
        - Tam hợp – xung chiếu – giáp cung

        Quy tắc:
        - KHÔNG mê tín
        - KHÔNG phán định tuyệt đối
        - Luận theo logic học thuật
        Dữ liệu lá số Tử Vi (JSON):
        {chart_json}
        Yêu cầu:
        1. Luận tổng quan cuộc đời
        2. Luận sự nghiệp – tài chính
        3. Luận tình cảm – hôn nhân
        4. Luận năm {nam_xem}
        5. Chỉ ra cung mạnh – cung yếu
        """
    try:
        result = llm.invoke(SYSTEM_PROMPT)
        if not isinstance(result, str):
            print("⚠️ Kết quả LLM không phải chuỗi")
            return None

        output = result.strip()

        if not output:
            print("⚠️ LLM trả về chuỗi rỗng")
            return None

        return output
    except subprocess.TimeoutExpired:
        print("⚠️ Ollama timeout sau 2 phút")
        return None
    except FileNotFoundError:
        print("⚠️ Không tìm thấy Ollama. Vui lòng cài đặt Ollama và đảm bảo nó có trong PATH.")
        return None
    except Exception as e:
        print(f"⚠️ Lỗi không mong đợi khi gọi Ollama: {str(e)}")
        return None