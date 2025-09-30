import streamlit as st
import json, os

# ========== 課程結構 ==========
course_structure = {
    "總體要求": {
        "畢業總學分": 128,
        "系訂必修學分": 56,
        "共同必修學分": 12,
        "通識學分": 24,
        "總選修學分": 48,
        "系內選修最低學分": 16,
        "通識至少領域數": 3
    },
    "課程": {
        "共同必修": {
            "國文上": 3, "國文下": 3, "英文一": 3, "英文二": 3,
            "進階英文一": 0, "進階英文二": 0,
            "體育一": 0, "體育二": 0, "體育三": 0, "體育四": 0,
            "服務學習甲": 0, "服務學習乙": 0
        },
        "系訂必修": {
            "微積分1": 2, "微積分2": 2, "微積分3": 2, "微積分4": 2,
            "普通物理學甲上": 3, "普通物理學甲下": 3,
            "普通物理學實驗上": 1, "普通物理學實驗下": 1,
            "普通化學一": 3, "普通化學二": 3,
            "化學實驗一": 1, "化學實驗二": 1,
            "分析化學一": 3, "分析化學二": 3,
            "有機化學一": 3, "有機化學二": 3,
            "化學實驗三": 2, "化學實驗四": 2,
            "物理化學二-量子化學": 3,
            "物理化學一-熱力學": 3,
            "化學實驗五": 2,
            "無機化學一": 3, "無機化學二": 3,
            "書報討論一": 1, "書報討論二": 1
        },
        "系內選修": {
            "大三專題討論一": 1, "大三專題討論二": 1,
            "大三專題研究一": 3, "大三專題研究二": 3,
            "大四專題討論一": 1, "大四專題討論二": 1,
            "大四專題研究一": 3, "大四專題研究二": 3,
            "大四論文": 1, "分析化學三": 3,
            "有機化學三": 3, "物理化學三-動力學": 3,
            "生物化學": 3, "材料化學": 3,
            "化學鍵": 2, "化學生物學": 2,
            "化學數學二": 2, "生物物理化學導論": 3,
            "有機合成": 3, "光學方法在生物研究之應用": 3
        },
        "通識課程": {
            "A1": {}, "A2": {}, "A3": {}, "A4": {},
            "A5": {}, "A6": {}, "A7": {}, "A8": {}
        }
    }
}

DATA_FILE = "ntu_my_courses.json"

# ========== 資料操作 ==========
def init_data():
    if not os.path.exists(DATA_FILE):
        save_data({"已修課程": {}})

def load_data():
    if not os.path.exists(DATA_FILE):
        init_data()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def find_course(name):
    for cat, courses in course_structure["課程"].items():
        if cat == "通識課程":
            for domain, domain_courses in courses.items():
                if name in domain_courses:
                    return cat, name, domain_courses[name]
        else:
            if name in courses:
                return cat, name, courses[name]
    return None, None, None

def add_course(name, credit=None, domain=None):
    data = load_data()
    if name in data["已修課程"]:
        return f"⚠️ 已登錄過：{name}"
    cat, cname, ccredit = find_course(name)
    if cname:
        data["已修課程"][cname] = {"學分": ccredit, "領域": None}
        save_data(data)
        return f"✅ 已新增：{cname}（{ccredit} 學分），分類：{cat}"
    else:
        if credit is None:
            return f"⚠️ {name} 需要輸入學分！"
        data["已修課程"][name] = {"學分": credit, "領域": domain if domain else None}
        save_data(data)
        return f"✅ 已新增：{name}（{credit} 學分），領域：{domain if domain else '無'}"

def delete_course(name):
    data = load_data()
    if name in data["已修課程"]:
        del data["已修課程"][name]
        save_data(data)
        return f"🗑 已刪除課程：{name}"
    else:
        return f"⚠️ 找不到課程：{name}"

def credits_by_category():
    data = load_data()
    cat_credits = {cat:0 for cat in course_structure["課程"]}
    cat_credits["自由選修"] = 0
    for c, info in data["已修課程"].items():
        domain = info.get("領域")
        if domain and domain.startswith("A"):  # 通識
           cat_credits["通識課程"] += info["學分"]
        else:
            found = False
            for cat, courses in course_structure["課程"].items():
                if cat=="通識課程":
                    continue
                if c in courses:
                    cat_credits[cat] += info["學分"]
                    found = True
                    break
            if not found:
                cat_credits["自由選修"] += info["學分"]
    return cat_credits

def graduation_check():
    d = load_data()
    req = course_structure["總體要求"]

    results = []
    # 總學分
    total = sum(info["學分"] for c, info in d["已修課程"].items())
    results.append(f"總學分：{total} / {req['畢業總學分']}")

    # 系訂必修
    required_courses = course_structure["課程"]["系訂必修"]
    taken_required = sum(info["學分"] for c, info in d["已修課程"].items() if c in required_courses)
    missing_required = [c for c in required_courses if c not in d["已修課程"]]
    results.append(f"系訂必修：{taken_required} / {req['系訂必修學分']}")
    if missing_required:
        results.append("▶️ 還沒修的系訂必修課程：" + "、".join(missing_required))

    # 共同必修
    common_required = course_structure["課程"]["共同必修"]
    taken_common = sum(info["學分"] for c, info in d["已修課程"].items() if c in common_required)
    missing_common = [c for c in common_required if c not in d["已修課程"]]
    results.append(f"共同必修：{taken_common} / {req['共同必修學分']}")
    if missing_common:
        results.append("▶️ 還沒修的共同必修課程：" + "、".join(missing_common))

    # 系內選修
    elective_courses = course_structure["課程"]["系內選修"]
    taken_elective = sum(info["學分"] for c, info in d["已修課程"].items() if c in elective_courses)
    missing_elective_credit = max(req["系內選修最低學分"] - taken_elective, 0)
    results.append(f"系內選修：{taken_elective} / {req['系內選修最低學分']} 學分")
    if missing_elective_credit > 0:
        results.append(f"⭐️ 還要修 {missing_elective_credit} 學分的系內選修！")

    # 總選修
    cat_credits = credits_by_category()
    total_elective = cat_credits["系內選修"] + cat_credits["自由選修"]
    missing_total_elective = max(req["總選修學分"] - total_elective, 0)
    results.append(f"總選修：{total_elective} / {req['總選修學分']}")
    if missing_total_elective > 0:
        results.append(f"⭐️ 還要修 {missing_total_elective} 學分的選修！")

    # 通識
    ge_total = 0
    ge_domains = set()
    for c, info in d["已修課程"].items():
        domain = info.get("領域")
        if domain and domain.startswith("A"):
            ge_total += info["學分"]
            ge_domains.add(domain)
    results.append(f"通識：{ge_total} / {req['通識學分']} 學分，涵蓋領域數 {len(ge_domains)} / {req['通識至少領域數']}")
    if ge_total < req["通識學分"]:
        results.append(f"⭐️ 通識還差 {req['通識學分'] - ge_total} 學分")

    return results

# ========== Streamlit UI ==========
st.title("🎓 學分檢查工具")

menu = st.sidebar.radio("功能選擇", ["新增課程", "刪除課程", "已修課程列表", "各類別學分", "畢業檢查"])

if menu == "新增課程":
    name = st.text_input("課程名稱")
    credit = st.number_input("學分（若課程結構已有，這裡可留 0）", min_value=0, max_value=10, value=0)
    domain = st.text_input("通識領域（A1–A8，非通識可留空）")
    if st.button("新增"):
        msg = add_course(name, credit if credit>0 else None, domain if domain else None)
        st.success(msg)

elif menu == "刪除課程":
    name = st.text_input("要刪除的課程名稱")
    if st.button("刪除"):
        msg = delete_course(name)
        st.success(msg)

elif menu == "已修課程列表":
    st.subheader("📚 已修課程")
    d = load_data()
    for c, info in d["已修課程"].items():
        st.write(f"- {c} ({info['學分']} 學分) 領域：{info.get('領域','無')}")

elif menu == "各類別學分":
    st.subheader("📊 各類別學分")
    stats = credits_by_category()
    for k,v in stats.items():
        st.write(f"{k}: {v}")

elif menu == "畢業檢查":
    st.subheader("✅ 畢業條件檢查")
    results = graduation_check()
    for r in results:
        st.write(r)
