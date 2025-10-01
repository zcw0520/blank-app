import json
import os
import streamlit as st

# ========== 課程結構 ==========
course_structure = {
    "總體要求": {
        "畢業總學分": 128,
        "系訂必修學分": 56,
        "共同必修學分": 9,
        "通識學分": 15,
        "總選修學分": 48,
        "系內選修最低學分": 16,
        "通識至少領域數": 3
    },
    "課程": {
        "共同必修": {
            "國文上": 3, "國文下": 3, "英文一": 3, "英文二": 3,
            "進階英文一": 0, "進階英文二": 0,
            "體育一": 2, "體育二": 2, "體育三": 2, "體育四": 2,
            "服務學習甲": 2, "服務學習乙": 2
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
        # 預設資料，包含你這學期修的課
        initial_data = {
            "已修課程": {
                "英文一": {"學分": 3, "領域": None},
                "體育一": {"學分": 2, "領域": None},
                "服務學習甲": {"學分": 2, "領域": None},
                "微積分1": {"學分": 2, "領域": None},
                "普通物理學甲上": {"學分": 3, "領域": None},
                "普通物理學實驗上": {"學分": 1, "領域": None},
                "普通化學一": {"學分": 3, "領域": None},
                "化學實驗一": {"學分": 1, "領域": None},
                "新生專題": {"學分": 2, "領域": None},
                "普通心理學": {"學分": 3, "領域": None}
            }
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=4)

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

# ========== 畢業檢查 ==========
def graduation_check():
    d = load_data()
    req = course_structure["總體要求"]
    results = []

    # 課程分類
    common_required = course_structure["課程"]["共同必修"]
    required_courses = course_structure["課程"]["系訂必修"]
    elective_courses = course_structure["課程"]["系內選修"]

    # 已修共同必修
    taken_common_courses = [c for c in common_required if c in d["已修課程"]]
    taken_common = sum(d["已修課程"][c]["學分"] for c in taken_common_courses)
    missing_common = [c for c in common_required if c not in d["已修課程"]]
    results.append(f"共同必修：已修 {len(taken_common_courses)} / 9 門課，共 {taken_common} 學分")
    if missing_common:
        results.append("▶️ 還沒修的共同必修課程：" + "、".join(missing_common))

    # 已修系訂必修
    taken_required = sum(info["學分"] for c, info in d["已修課程"].items() if c in required_courses)
    missing_required = [c for c in required_courses if c not in d["已修課程"]]
    results.append(f"系訂必修：已修 {taken_required} / {req['系訂必修學分']} 學分")
    if missing_required:
        results.append("▶️ 還沒修的系訂必修課程：" + "、".join(missing_required))

    # 系內選修
    taken_elective = sum(info["學分"] for c, info in d["已修課程"].items() if c in elective_courses)
    free_elective = sum(info["學分"] for c, info in d["已修課程"].items()
                        if c not in elective_courses and c not in required_courses and c not in common_required and not (info.get("領域","").startswith("A")))
    total_elective = taken_elective + free_elective
    results.append(f"系內/自由選修：已修 {total_elective} / {req['總選修學分']} 學分")
    if taken_elective < req["系內選修最低學分"]:
        results.append(f"⭐️ 還要修 {req['系內選修最低學分'] - taken_elective} 學分的系內選修！")
    if total_elective < req["總選修學分"]:
        results.append(f"⭐️ 還要修 {req['總選修學分'] - total_elective} 學分的選修！")

    # 通識學分與國文抵扣
    ge_total = 0
    ge_domains = set()
    for c, info in d["已修課程"].items():
        domain = info.get("領域")
        if domain and domain.startswith("A"):
            ge_total += info["學分"]
            ge_domains.add(domain)

    chinese_credit = 0
    if "國文上" in d["已修課程"]:
        chinese_credit += 3
    if "國文下" in d["已修課程"]:
        chinese_credit += 3

    deductible = 0
    for dom in ["A1","A2","A3","A4"]:
        for c, info in d["已修課程"].items():
            if info.get("領域")==dom:
                deductible = min(chinese_credit,3)
                break

    actual_ge = max(ge_total - deductible,0)
    results.append(f"通識：已修 {actual_ge} / {req['通識學分']} 學分，涵蓋領域數 {len(ge_domains)} / {req['通識至少領域數']}")
    if actual_ge < req["通識學分"]:
        results.append(f"⭐️ 通識還差 {req['通識學分'] - actual_ge} 學分")

    # 總畢業學分
    total_credits = taken_common + actual_ge + taken_required + total_elective
    results.insert(0, f"總畢業學分：{total_credits} / {req['畢業總學分']}")

    return results

# ========== Streamlit UI ==========
st.title("🎓 學分檢查工具")

menu = st.sidebar.radio("功能選擇", ["新增課程", "刪除課程", "已修課程列表", "畢業檢查"])

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

elif menu == "畢業檢查":
    st.subheader("✅ 畢業條件檢查")
    results = graduation_check()
    for r in results:
        st.write(r)
