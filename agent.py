from core.core import build_tuvi_engine
from llm.prompt import ask_llm
chart =  build_tuvi_engine(
    day=15,
    month=7,
    year=2006,
    hour=8,
    minute=40,      # 8h40 vẫn là giờ Thìn
    gender="Nam",
    nam_xem=2026
)

analysis = ask_llm(chart_json=chart,nam_xem=2026)
print("===== KẾT QUẢ LUẬN GIẢI =====")
print(analysis)