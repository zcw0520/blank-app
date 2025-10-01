import json
import os
import streamlit as st
import pandas as pd

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
            "國文上": 3, "英文一": 3, "英文二": 3,
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
            "(A1)文學與藝術": {}, 
            "(A2)歷史思維": {}, 
            "(A3)世界文明": {}, 
            "(A4)哲學與道德思考": {}, 
            "(A5)公民意識與社會分析": {}, 
            "(A8)生命科學": {}
        }
    }
}

DATA_FILE = "ntu_my_courses.json"

# ========== 資料操作 ==========
def init_data():
    if not os.path.exists(DATA_FILE):
        initial_data = {
            "已修課程": {
                "英文一": {"學分": 3, "領域": None},
                "體育一": {"學分": 0, "領域": None},
                "服務學習甲": {"學分": 0, "領域": None},
                "微積分1": {"學分": 2, "領域": None},
                "普通物理學甲上": {"學分": 3, "領域": None},
                "普通物理學實驗上": {"學分": 1, "領域": None},
                "普通化學一": {"學分": 3, "領域": None},
                "化學實驗一": {"學分": 1, "領域": None},
                "新生專題": {"學分": 2, "領域": None},
                "普通心理學": {"學分": 3, "領域": "公民意識與社會分析(A5)"}
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

elif menu == "畢業檢查":
    st.subheader("✅ 畢業條件檢查")

    # 載入資料
    d = load_data()

    # 計算各類學分
    common_required = course_structure["課程"]["共同必修"]
    required_courses = course_structure["課程"]["系訂必修"]
    elective_courses = course_structure["課程"]["系內選修"]

    taken_common = sum(d["已修課程"][c]["學分"] for c in common_required if c in d["已修課程"])
    taken_required = sum(d["已修課程"][c]["學分"] for c in required_courses if c in d["已修課程"])
    taken_elective = sum(d["已修課程"][c]["學分"] for c in elective_courses if c in d["已修課程"])
    free_elective = sum(
        info["學分"] for c, info in d["已修課程"].items()
        if c not in elective_courses and c not in required_courses and c not in common_required
    )
    total_elective = taken_elective + free_elective

    ge_total = sum(info["學分"] for c, info in d["已修課程"].items() if info.get("領域") and "(A" in info["領域"])
    chinese_credit = sum(d["已修課程"][c]["學分"] for c in ["國文上","國文下"] if c in d["已修課程"])
    deductible = min(chinese_credit, 3) if ge_total>0 else 0
    actual_ge = max(ge_total - deductible,0)

    total_credits = taken_common + taken_required + total_elective + actual_ge

    # 顯示進度條
    st.progress(total_credits / 128)

    # 顯示學分表格
    st.table({
        "總學分": f"{total_credits} / 128",
        "共同必修": f"{taken_common} / 9",
        "系訂必修": f"{taken_required} / 56",
        "選修": f"{total_elective} / 48",
        "通識": f"{actual_ge} / 15"
    })


    common_required = course_structure["課程"]["共同必修"]
    required_courses = course_structure["課程"]["系訂必修"]
    elective_courses = course_structure["課程"]["系內選修"]

    # 共同必修
    taken_common_courses = [c for c in common_required if c in d["已修課程"]]
    taken_common = sum(d["已修課程"][c]["學分"] for c in taken_common_courses)

    # 系訂必修
    taken_required = sum(info["學分"] for c, info in d["已修課程"].items() if c in required_courses)

    # 選修
    taken_elective = sum(info["學分"] for c, info in d["已修課程"].items() if c in elective_courses)
    free_elective = sum(
        info["學分"]
        for c, info in d["已修課程"].items()
        if c not in elective_courses
        and c not in required_courses
        and c not in common_required
        and not (info.get("領域") and "(A" in str(info["領域"]))
    )
    total_elective = taken_elective + free_elective

    # 通識
    ge_total = 0
    ge_domains = set()
    for c, info in d["已修課程"].items():
        domain = str(info.get("領域", ""))
        if "(A" in domain:
            ge_total += info["學分"]
            ge_domains.add(domain)
    chinese_credit = 0
    if "國文上" in d["已修課程"]:
        chinese_credit += 3
    if "國文下" in d["已修課程"]:
        chinese_credit += 3
    deductible = min(chinese_credit, 3) if ge_total > 0 else 0
    actual_ge = max(ge_total - deductible, 0)

    # 總學分
    total_credits = taken_common + actual_ge + taken_required + total_elective

    # 回傳整數數據
    return int(total_credits), int(taken_common), int(taken_required), int(total_elective), int(actual_ge), len(ge_domains)

# ========== Streamlit UI ==========
st.title("🎓 學分檢查工具")

menu = st.sidebar.radio("功能選擇", ["新增課程", "刪除課程", "已修課程列表", "畢業檢查"])

if menu == "新增課程":
    name = st.text_input("課程名稱")
    credit = st.number_input("學分（若課程結構已有，這裡可留 0）", min_value=0, max_value=10, value=0)
    ge_options = [
        "非通識",
        "(A1)文學與藝術", 
        "(A2)歷史思維", 
        "(A3)世界文明", 
        "(A4)哲學與道德思考", 
        "(A5)公民意識與社會分析", 
        "(A8)生命科學"
    ]
    domain = st.selectbox("通識領域", ge_options, index=0)
    if domain == "非通識":
        domain = None
    if st.button("新增"):
        msg = add_course(name, credit if credit>0 else None, domain)
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
    total_credits, taken_common, taken_required, total_elective, actual_ge, ge_domains_count = graduation_check()

    # 顯示進度條
    progress = min(total_credits / course_structure["總體要求"]["畢業總學分"], 1.0)
    st.progress(progress)

   # 顯示表格（幾分之幾）
df = pd.DataFrame([{
    "總學分": f"{total_credits} / 128",
    "共同必修": f"{taken_common} / 9",
    "系訂必修": f"{taken_required} / 56",
    "選修": f"{total_elective} / 48",
    "通識": f"{actual_ge} / 15",
    "涵蓋通識領域數": f"{ge_domains_count} / 3"
}])
st.table(df)

# 在畢業檢查區塊
d = load_data()
common_required = course_structure["課程"]["共同必修"]
required_courses = course_structure["課程"]["系訂必修"]
elective_courses = course_structure["課程"]["系內選修"]

# 生成未修課程表格
missing_data = []

missing_common = [c for c in common_required if c not in d["已修課程"]]
for c in missing_common:
    missing_data.append({"類別": "共同必修", "課程名稱": c})

missing_required = [c for c in required_courses if c not in d["已修課程"]]
for c in missing_required:
    missing_data.append({"類別": "系訂必修", "課程名稱": c})

missing_elective = [c for c in elective_courses if c not in d["已修課程"]]
for c in missing_elective:
    missing_data.append({"類別": "系內選修", "課程名稱": c})

if missing_data:
    st.subheader("📋 未修課程")
    df_missing = pd.DataFrame(missing_data)
    st.table(df_missing)
else:
    st.success("🎉 所有必修課程已完成！")
