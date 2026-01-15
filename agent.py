from core.core import build_tuvi_engine

from tuvi_rag import analyze_tuvi

chart =  build_tuvi_engine(
    day=15,
    month=7,
    year=2006,
    hour=8,
    minute=40,      # 8h40 vẫn là giờ Thìn
    gender="Nam",
    nam_xem=2026
)

result = analyze_tuvi(chart_result=chart,year=2026)

print("===== KẾT QUẢ LUẬN GIẢI =====")

print(result)