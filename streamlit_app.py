import json
import os
import difflib
import streamlit as st

# ========== 資料檔案 ==========
DATA_FILE = "my_courses_data.json"

# ========== 課程結構與學分規範 ==========
course_structure = {
    "校核心必修": {
        "中文閱讀與書寫(一)": 2,
        "中文閱讀與書寫(二)": 2,
        "英文(一)": 3,
        "英文(二)": 3
    },
    "院核心必修": {
        "組織與社會": 2,
        "運算思維與程式設計": 2
    },
    "系基礎必修": {
        "政治學": 3,
        "行政學": 3,
        "經濟學": 3,
        "法學緒論": 3,
        "中華民國憲法與政府": 3,
        "管理學": 3,
        "統計學": 3,
        "社會科學研究法": 3,
        "專題與實習": 3
    },
    "系基礎選修": {
        "企業概論": 3,
        "社會學": 3,
        "會計學": 3,
        "應用統計學": 3,
        "行政管理理論": 2,
        "政治經濟學": 3
    },
    "系核心課程": {
        "組織管理學群": {
            "組織理論與管理": 3,
            "公共管理": 2,
            "組織行為": 3
        },
        "公私決策學群": {
            "公共政策(一)": 2,
            "公共政策(二)": 2,
            "問題分析與決策": 2
        },
        "地區發展與行銷學群": {
            "行銷管理": 3,
            "消費者行為": 3,
            "都市與地方治理": 3
        }
    },
    "通識領域": {
        "文史哲藝術": {
            "美國文化": 2,
            "英文小品文賞析": 2
        },
        "社會脈動": {
            "法律素養": 2,
            "犯罪、法律與人權": 2
        },
        "生命科學": {
            "ESG與永續生活設計": 2,
            "水資源利用與保育": 2
        },
        "科技探索": {
            "AI人文藝術之應用": 2,
            "大數據分析概論": 2
        }
    },
    "自由選修": {}
}

graduation_req = {
    "總學分": 132,
    "校核心": 10,
    "院核心": 4,
    "系基礎必修": 27,
    "系基礎選修": 23,
    "系核心課程": 10,
    "選修總學分": 18,
    "自由選修": 20,
    "通識領域數": 3
}

# ========== 資料存取 ==========
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

# ========== 工具函數 ==========
def find_course(name):
    for cat, courses in course_structure.items():
        if cat == "系核心課程":
            for group, group_courses in courses.items():
                if name in group_courses:
                    return f"{cat}-{group}", name, group_courses[name]
        elif cat == "通識領域":
            for domain, domain_courses in courses.items():
                if name in domain_courses:
                    return f"{cat}-{domain}", name, domain_courses[name]
        else:
            if name in courses:
                return cat, name, courses[name]
    return None, None, None

# ========== Streamlit UI ==========
st.set_page_config(page_title="畢業學分檢查系統", layout="wide")
st.title("🎓 畢業學分檢查系統")

data = load_data()

tab1, tab2 = st.tabs(["➕ 新增課程", "📊 畢業檢查"])

with tab1:
    st.subheader("新增已修課程")
    course_input = st.text_input("課程名稱")
    credit_input = st.number_input("學分（可自行輸入，預設為課程結構學分）", min_value=1, step=1)
    if st.button("加入"):
        if course_input:
            cat, cname, credit = find_course(course_input)
            if cname:
                data["已修課程"][cname] = credit_input if credit_input else credit
                save_data(data)
                st.success(f"✅ 已加入 {cname} ({data['已修課程'][cname]}學分)")
            else:
                data["已修課程"][course_input] = credit_input
                save_data(data)
                st.success(f"✅ 已加入自訂課程 {course_input} ({credit_input}學分)")

    st.subheader("📖 已修課程列表")
    if data["已修課程"]:
        for c, cr in data["已修課程"].items():
            st.write(f"- {c} ({cr}學分)")
        del_course = st.text_input("刪除課程名稱（單筆）")
        if st.button("刪除課程"):
            if del_course in data["已修課程"]:
                data["已修課程"].pop(del_course)
                save_data(data)
                st.success(f"🗑 已刪除 {del_course}")
            else:
                st.warning("⚠️ 找不到課程")
    else:
        st.write("尚未加入課程")

with tab2:
    st.subheader("📊 畢業檢查報告")
    taken = data["已修課程"]

    # 計算各類學分
    def sum_category(cat):
        total = 0
        if cat == "系核心課程":
            for group, group_courses in course_structure["系核心課程"].items():
                for c in group_courses:
                    if c in taken:
                        total += taken[c]
        elif cat == "通識領域":
            for domain, domain_courses in course_structure["通識領域"].items():
                for c in domain_courses:
                    if c in taken:
                        total += taken[c]
        else:
            for c in course_structure.get(cat, {}):
                if c in taken:
                    total += taken[c]
        return total

    # 校核心
    core_sch = sum_category("校核心必修")
    st.metric("校核心已修學分", core_sch, delta=f"需求 {graduation_req['校核心']}")

    # 院核心
    core_col = sum_category("院核心必修")
    st.metric("院核心已修學分", core_col, delta=f"需求 {graduation_req['院核心']}")

    # 系基礎必修
    dept_req = sum_category("系基礎必修")
    st.metric("系基礎必修已修學分", dept_req, delta=f"需求 {graduation_req['系基礎必修']}")

    # 系基礎選修
    dept_elective = sum_category("系基礎選修")
    st.metric("系基礎選修已修學分", dept_elective, delta=f"需求 {graduation_req['系基礎選修']}")

    # 系核心三領域
    st.write("### 系核心課程三領域")
    for group in course_structure["系核心課程"]:
        total = 0
        for c in course_structure["系核心課程"][group]:
            if c in taken:
                total += taken[c]
        st.metric(group, total, delta=f"需求 ≥ {graduation_req['系核心課程']}")

    # 通識
    st.write("### 通識領域")
    for domain in course_structure["通識領域"]:
        total = 0
        for c in course_structure["通識領域"][domain]:
            if c in taken:
                total += taken[c]
        st.metric(domain, total, delta="需求 ≥ 2")

    # 自由選修
    free = 0
    all_known = []
    for cat, courses in course_structure.items():
        if cat not in ["校核心必修", "院核心必修", "系基礎必修", "系基礎選修", "系核心課程", "通識領域"]:
            all_known += list(courses.keys())
    for c in taken:
        if c not in all_known:
            free += taken[c]
    st.metric("自由選修", free, delta=f"需求 ≥ {graduation_req['自由選修']}")

    # 總學分
    total = sum(taken.values())
    st.metric("已修總學分", total, delta=f"畢業需求 {graduation_req['總學分']}")
