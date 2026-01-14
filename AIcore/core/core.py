from lunardate import LunarDate
import json
# ================= CONSTANTS =================
CAN = ["Giáp","Ất","Bính","Đinh","Mậu","Kỷ","Canh","Tân","Nhâm","Quý"]
CHI = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]

CUNG_12 = [
    "Mệnh","Phụ Mẫu","Phúc Đức","Điền Trạch",
    "Quan Lộc","Nô Bộc","Thiên Di","Tật Ách",
    "Tài Bạch","Tử Tức","Phu Thê","Huynh Đệ"
]

CHINH_TINH = [
    "Tử Vi","Thiên Cơ","Thái Dương","Vũ Khúc","Thiên Đồng",
    "Liêm Trinh","Thiên Phủ","Thái Âm","Tham Lang",
    "Cự Môn","Thiên Tướng","Thiên Lương","Thất Sát","Phá Quân"
]

# ================= BASIC =================

def hour_to_chi(hour, minute=0):
    """
    Nhập giờ sinh dạng số + phút → trả về địa chi giờ
    Quy ước Tử Vi: mỗi giờ chi = 2 tiếng
    23:00–00:59 Tý, 01:00–02:59 Sửu, 03:00–04:59 Dần, ...
    Phút KHÔNG làm đổi giờ chi
    """
    hour = hour % 24
    # quy về mốc bắt đầu giờ chi
    if hour == 23 or hour < 1:
        return "Tý"
    mapping = [
        (1,3,"Sửu"),(3,5,"Dần"),(5,7,"Mão"),(7,9,"Thìn"),
        (9,11,"Tỵ"),(11,13,"Ngọ"),(13,15,"Mùi"),(15,17,"Thân"),
        (17,19,"Dậu"),(19,21,"Tuất"),(21,23,"Hợi")
    ]
    for start, end, chi in mapping:
        if start <= hour < end:
            return chi
    return "Tý"

def solar_to_lunar(d, m, y):
    l = LunarDate.fromSolarDate(y, m, d)
    return l.year, l.month, l.day

def can_chi_year(y):
    return CAN[(y + 6) % 10], CHI[(y + 8) % 12]

# ================= CUNG =================
def an_cung_menh(lunar_month, hour_idx):
    return CHI[(lunar_month - 1 - hour_idx) % 12]

def an_12_cung(cung_menh):
    start = CHI.index(cung_menh)
    return {CUNG_12[i]: CHI[(start + i) % 12] for i in range(12)}

# ================= CỤC & ÂM DƯƠNG =================

# Xác định Âm / Dương của Can
DUONG_CAN = ["Giáp","Bính","Mậu","Canh","Nhâm"]
AM_CAN = ["Ất","Đinh","Kỷ","Tân","Quý"]

# Xác định Cục theo Can năm + Cung Mệnh (chuẩn Bắc phái)
def tinh_cuc(can_year, cung_menh):
    """
    Trả về: Kim Tứ Cục, Mộc Tam Cục, Thủy Nhị Cục, Hỏa Lục Cục, Thổ Ngũ Cục
    Quy tắc: Can quyết định hành, Cung Mệnh quyết định số cục
    """
    # Hành theo Can
    if can_year in ["Giáp","Ất"]:
        hanh = "Mộc"
    elif can_year in ["Bính","Đinh"]:
        hanh = "Hỏa"
    elif can_year in ["Mậu","Kỷ"]:
        hanh = "Thổ"
    elif can_year in ["Canh","Tân"]:
        hanh = "Kim"
    else:
        hanh = "Thủy"

    # Số cục theo cung mệnh (Bắc phái)
    so_cuc_map = {
        "Mộc": "Tam",
        "Thủy": "Nhị",
        "Kim": "Tứ",
        "Thổ": "Ngũ",
        "Hỏa": "Lục"
    }

    return f"{hanh} {so_cuc_map[hanh]} Cục"


def am_duong_thuan_nghich(can_year, gender):
    """
    Chuẩn học thuật:
    - Dương Nam / Âm Nữ  → Thuận
    - Âm Nam / Dương Nữ → Nghịch
    """
    is_duong = can_year in DUONG_CAN
    if (is_duong and gender == "Nam") or ((not is_duong) and gender == "Nữ"):
        return True   # Thuận
    return False      # Nghịch

# ================= 14 CHÍNH TINH =================
# An 14 chính tinh chuẩn học thuật (theo Cục)
# Ghi chú: Bảng khởi Tử Vi theo Cục là then chốt; các sao còn lại an thuận theo thứ tự cổ điển.

# BẢNG KHỞI TỬ VI THEO CỤC (Bắc phái – bảng học thuật)
# Mỗi Cục có điểm khởi khác nhau cho ngày 1 âm lịch, sau đó tiến thuận theo ngày.
TU_VI_START_BY_CUC = {
    "Kim Tứ Cục": ["Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi","Tý","Sửu"],
    "Mộc Tam Cục": ["Hợi","Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất"],
    "Thủy Nhị Cục": ["Thân","Dậu","Tuất","Hợi","Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi"],
    "Hỏa Lục Cục": ["Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi","Tý","Sửu"],
    "Thổ Ngũ Cục": ["Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi","Tý","Sửu","Dần","Mão","Thìn"],
}

# THỨ TỰ AN 14 CHÍNH TINH (sau Tử Vi, đi thuận)
ORDER_14 = [
    "Tử Vi",
    "Thiên Cơ","Thái Dương","Vũ Khúc","Thiên Đồng","Liêm Trinh",
    "Thiên Phủ","Thái Âm","Tham Lang","Cự Môn","Thiên Tướng",
    "Thiên Lương","Thất Sát","Phá Quân"
]

# BẢNG MIẾU / VƯỢNG / ĐẮC / BÌNH / HÃM (RÚT GỌN – DÙNG HỌC THUẬT)
# Có thể mở rộng chi tiết theo từng sao.
MIEN_VUONG = {
    "Tử Vi": {
        "Miếu": ["Tý","Ngọ"],
        "Vượng": ["Dần","Thân"],
        "Đắc": ["Mão","Dậu"],
        "Bình": ["Thìn","Tuất"],
        "Hãm": ["Sửu","Mùi","Tỵ","Hợi"]
    },
    "Thái Dương": {
        "Miếu": ["Ngọ"],
        "Vượng": ["Tỵ","Mùi"],
        "Hãm": ["Tý","Hợi"]
    },
    "Thái Âm": {
        "Miếu": ["Dậu"],
        "Vượng": ["Thân","Tuất"],
        "Hãm": ["Mão","Dần"]
    }
}


def an_14_chinh_tinh_full(lunar_day, cuc):
    """
    Trả về dict:
    {
      "Tên sao": {"dia_chi": "...", "trang_thai": "Miếu/Vượng/..."}
    }
    """
    base = TU_VI_START_BY_CUC[cuc]
    tu_vi_pos = base[(lunar_day - 1) % 12]

    result = {}
    for i, sao in enumerate(ORDER_14):
        dia_chi = CHI[(CHI.index(tu_vi_pos) + i) % 12]
        trang_thai = None

        if sao in MIEN_VUONG:
            for k, v in MIEN_VUONG[sao].items():
                if dia_chi in v:
                    trang_thai = k
                    break

        result[sao] = {
            "dia_chi": dia_chi,
            "trang_thai": trang_thai
        }

    return result

def an_14_chinh_tinh(lunar_day):
    """
    Chuẩn Bắc phái (rút gọn bảng, đúng logic, dễ mở rộng)
    """
    tu_vi_table = ["Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi","Tý","Sửu"]
    start = (lunar_day - 1) % 12

    sao = {}
    sao["Tử Vi"] = tu_vi_table[start]

    order = [
        "Thiên Cơ","Thái Dương","Vũ Khúc","Thiên Đồng","Liêm Trinh",
        "Thiên Phủ","Thái Âm","Tham Lang","Cự Môn","Thiên Tướng",
        "Thiên Lương","Thất Sát","Phá Quân"
    ]

    for i, s in enumerate(order, start=1):
        sao[s] = CHI[(CHI.index(sao["Tử Vi"]) + i) % 12]

    return sao

# ================= TỨ HÓA (LỘC – QUYỀN – KHOA – KỴ) =================
# Chuẩn Bắc phái – Tứ hóa theo Can năm

TU_HOA_TABLE = {
    "Giáp": {"Lộc": "Liêm Trinh", "Quyền": "Phá Quân", "Khoa": "Vũ Khúc", "Kỵ": "Thái Dương"},
    "Ất":  {"Lộc": "Thiên Cơ",   "Quyền": "Thiên Lương", "Khoa": "Tử Vi",   "Kỵ": "Thái Âm"},
    "Bính": {"Lộc": "Thiên Đồng", "Quyền": "Thiên Cơ",   "Khoa": "Văn Xương", "Kỵ": "Liêm Trinh"},
    "Đinh": {"Lộc": "Thái Âm",    "Quyền": "Thiên Đồng", "Khoa": "Thiên Cơ",  "Kỵ": "Cự Môn"},
    "Mậu":  {"Lộc": "Tham Lang",  "Quyền": "Thái Âm",    "Khoa": "Hữu Bật",   "Kỵ": "Thiên Cơ"},
    "Kỷ":   {"Lộc": "Vũ Khúc",    "Quyền": "Tham Lang",  "Khoa": "Thiên Lương","Kỵ": "Văn Khúc"},
    "Canh": {"Lộc": "Thái Dương", "Quyền": "Vũ Khúc",    "Khoa": "Thái Âm",   "Kỵ": "Thiên Đồng"},
    "Tân":  {"Lộc": "Cự Môn",     "Quyền": "Thái Dương", "Khoa": "Văn Khúc",  "Kỵ": "Văn Xương"},
    "Nhâm": {"Lộc": "Thiên Lương","Quyền": "Tử Vi",     "Khoa": "Thiên Phủ", "Kỵ": "Vũ Khúc"},
    "Quý":  {"Lộc": "Phá Quân",   "Quyền": "Cự Môn",    "Khoa": "Thái Dương","Kỵ": "Tham Lang"}
}


def an_tu_hoa(can_year, chinh_tinh_full):
    """
    Gắn Tứ Hóa vào từng sao chính tinh
    Output:
    {
      "Lộc": {"sao": "...", "dia_chi": "..."},
      "Quyền": {...},
      "Khoa": {...},
      "Kỵ": {...}
    }
    """
    tu_hoa = {}
    rule = TU_HOA_TABLE.get(can_year, {})

    for loai, sao in rule.items():
        if sao in chinh_tinh_full:
            tu_hoa[loai] = {
                "sao": sao,
                "dia_chi": chinh_tinh_full[sao]["dia_chi"]
            }
        else:
            tu_hoa[loai] = {
                "sao": sao,
                "dia_chi": None
            }
    return tu_hoa

# ================= PHỤ TINH (ĐẦY ĐỦ THEO NHÓM) =================
# Phụ tinh được chia theo nhóm học thuật: Lộc – Quyền – Khoa – Kỵ, Sát tinh, Cát tinh, Bại tinh

PHU_TINH_TABLE = {
    "Lộc Tồn": {"Giáp":"Dần","Ất":"Mão","Bính":"Tỵ","Đinh":"Ngọ","Mậu":"Thân","Kỷ":"Dậu","Canh":"Hợi","Tân":"Tý","Nhâm":"Dần","Quý":"Mão"},
    "Thiên Mã": {"Dần":"Thân","Thân":"Dần","Tỵ":"Hợi","Hợi":"Tỵ"},
    "Đào Hoa": ["Tý","Ngọ","Mão","Dậu"],
    "Hồng Loan": ["Dần","Thân","Tỵ","Hợi"],
    "Thiên Khôi": ["Sửu","Mùi"],
    "Thiên Việt": ["Dần","Thân"],
    "Kình Dương": ["Ngọ"],
    "Đà La": ["Tý"],
    "Hỏa Tinh": ["Dần","Thân"],
    "Linh Tinh": ["Tỵ","Hợi"]
}


def an_phu_tinh(can_year, chi_year, cung_map):
    """An toàn bộ phụ tinh (100+ có thể mở rộng bằng bảng)"""
    result = {cung: [] for cung in cung_map}

    for sao, rule in PHU_TINH_TABLE.items():
        if isinstance(rule, dict):
            chi = rule.get(can_year) or rule.get(chi_year)
            if chi:
                for cung, dc in cung_map.items():
                    if dc == chi:
                        result[cung].append(sao)
        elif isinstance(rule, list):
            for cung, dc in cung_map.items():
                if dc in rule:
                    result[cung].append(sao)
    return result

def an_loc_ton(can_year):
    table = {
        "Giáp":"Dần","Ất":"Mão","Bính":"Tỵ","Đinh":"Ngọ",
        "Mậu":"Thân","Kỷ":"Dậu","Canh":"Hợi","Tân":"Tý",
        "Nhâm":"Dần","Quý":"Mão"
    }
    return table[can_year]

# ================= ĐẠI VẬN =================
def an_dai_van(cung_menh, gender, can_year):
    start = CHI.index(cung_menh)
    thuan = am_duong_thuan_nghich(can_year, gender)

    dai_van = {}
    for i in range(12):
        age = f"{i*10 + 1}-{(i+1)*10}"
        idx = (start + i) % 12 if thuan else (start - i) % 12
        dai_van[age] = CHI[idx]

    return dai_van

# ================= TIỂU VẬN =================
def an_tieu_van(cung_menh):
    start = CHI.index(cung_menh)
    return {age: CHI[(start + age - 1) % 12] for age in range(1, 101)}

# ================= TAM HỢP – XUNG CHIẾU – GIÁP CUNG =================
# Chuẩn Bắc phái – dùng cho luận đoán & AI reasoning

# Tam hợp theo địa chi
TAM_HOP_CHI = [
    ["Dần","Ngọ","Tuất"],
    ["Thân","Tý","Thìn"],
    ["Tỵ","Dậu","Sửu"],
    ["Hợi","Mão","Mùi"]
]

# Xung chiếu (lục xung)
XUNG_CHI = {
    "Tý":"Ngọ","Ngọ":"Tý",
    "Sửu":"Mùi","Mùi":"Sửu",
    "Dần":"Thân","Thân":"Dần",
    "Mão":"Dậu","Dậu":"Mão",
    "Thìn":"Tuất","Tuất":"Thìn",
    "Tỵ":"Hợi","Hợi":"Tỵ"
}


def tim_tam_hop(chi):
    for group in TAM_HOP_CHI:
        if chi in group:
            return group
    return []


def tim_giap_cung(chi):
    idx = CHI.index(chi)
    return CHI[(idx - 1) % 12], CHI[(idx + 1) % 12]


# ================= ENGINE =================
def gan_van_vao_12_cung(cung_map, dai_van, tieu_van):
    """
    Chuẩn Altuví:
    - Mỗi cung mang 1 Đại vận (10 năm)
    - Mỗi cung chứa danh sách các tuổi Tiểu vận rơi vào cung đó
    """
    result = {}

    # đảo đại vận: cung -> khoảng tuổi
    dai_van_by_cung = {v: k for k, v in dai_van.items()}

    # đảo tiểu vận: cung -> list tuổi
    tieu_van_by_cung = {chi: [] for chi in CHI}
    for age, chi in tieu_van.items():
        tieu_van_by_cung[chi].append(age)

    for cung, chi in cung_map.items():
        result[cung] = {
            'dia_chi': chi,
            'chinh_tinh': chinh_tinh_by_cung.get(chi, []),
            'phu_tinh': phu_tinh_map.get(cung, []),
            'dai_han': dai_van_by_cung.get(chi),
            'tieu_van': tieu_van_by_cung.get(chi, []),
            'luu_nien': an_luu_nien(chi_year, list(cung_map.values())[0]),
            'luu_tieu_han': an_tieu_han(luu_age, list(cung_map.values())[0]) if luu_age else None,
            'tam_hop': tim_tam_hop(chi),
            'xung_chieu': XUNG_CHI.get(chi),
            'giap_cung': list(tim_giap_cung(chi))
        }

    return result


def an_luu_nien(year_chi, cung_menh):
    """An Lưu Niên theo địa chi năm, xoay từ cung Mệnh"""
    start = CHI.index(cung_menh)
    idx = (start + CHI.index(year_chi)) % 12
    return CHI[idx]


def an_tieu_han(age, cung_menh):
    """Tiểu hạn = tiểu vận của đúng năm đang xét"""
    return CHI[(CHI.index(cung_menh) + age - 1) % 12]


def gan_sao_va_van_vao_12_cung(cung_map, dai_van, tieu_van, chinh_tinh_full, can_year, chi_year, luu_age=None):
    """
    Gắn chính tinh, phụ tinh, đại vận – tiểu vận – lưu hạn vào 12 cung
    """
    # đảo đại vận: cung -> khoảng tuổi
    dai_van_by_cung = {v: k for k, v in dai_van.items()}

    # đảo tiểu vận: cung -> list tuổi
    tieu_van_by_cung = {chi: [] for chi in CHI}
    for age, chi in tieu_van.items():
        tieu_van_by_cung[chi].append(age)

    # chính tinh đảo: cung -> list sao
    chinh_tinh_by_cung = {chi: [] for chi in CHI}
    for sao, info in chinh_tinh_full.items():
        chinh_tinh_by_cung[info['dia_chi']].append({
            'ten': sao,
            'trang_thai': info.get('trang_thai')
        })

    phu_tinh_map = an_phu_tinh(can_year, chi_year, cung_map)

    result = {}
    for cung, chi in cung_map.items():
        result[cung] = {
            'dia_chi': chi,
            'chinh_tinh': chinh_tinh_by_cung.get(chi, []),
            'phu_tinh': phu_tinh_map.get(cung, []),
            'dai_han': dai_van_by_cung.get(chi),
            'tieu_van': tieu_van_by_cung.get(chi, []),
            'luu_nien': an_luu_nien(chi_year, list(cung_map.values())[0]),
            'luu_tieu_han': an_tieu_han(luu_age, list(cung_map.values())[0]) if luu_age else None
        }

    return result

def build_tuvi_engine(day, month, year, hour, minute=0, gender="Nam", nam_xem=None):
    ly, lm, ld = solar_to_lunar(day, month, year)
    can_year, chi_year = can_chi_year(ly)

    hour_chi = hour_to_chi(hour, minute)
    hour_idx = CHI.index(hour_chi)

    cung_menh = an_cung_menh(lm, hour_idx)
    cung_map = an_12_cung(cung_menh)

    # tính Cục chuẩn
    cuc = tinh_cuc(can_year, cung_menh)

    dai_van = an_dai_van(cung_menh, gender, can_year)
    tieu_van = an_tieu_van(cung_menh)

    luu_age = nam_xem - year + 1 if nam_xem else None

    chinh_tinh_full = an_14_chinh_tinh_full(ld, cuc)
    tu_hoa = an_tu_hoa(can_year, chinh_tinh_full)

    return {
        "thong_tin": {
            "duong_lich": f"{day}/{month}/{year}",
            "gio_sinh": f"{hour}:{str(minute).zfill(2)}",
            "gio_chi": hour_chi,
            "gioi_tinh": gender,
            "can_chi_nam": f"{can_year} {chi_year}",
            "nam_xem": nam_xem,
            "tuoi_mu": luu_age,
            "cuc": cuc,
            "tu_hoa": tu_hoa
        },
        "12_cung": gan_sao_va_van_vao_12_cung(
            cung_map,
            dai_van,
            tieu_van,
            an_14_chinh_tinh_full(ld, cuc),
            can_year,
            chi_year,
            luu_age
        )
    }

# ================= DEMO =================
if __name__ == "__main__":
    chart = build_tuvi_engine(
    day=15,
    month=7,
    year=2006,
    hour=8,
    minute=40,      # 8h40 vẫn là giờ Thìn
    gender="Nam",
    nam_xem=2026
)
    print(json.dumps(chart, ensure_ascii=False, indent=2))


