import json
import os
import streamlit as st

# ================== 資料檔案 ==================
DATA_FILE = "my_courses.json"

# ================== 課程結構 ==================
course_structure = {
    "校核心必修": {
        "中文閱讀與書寫(一)": 2,
        "中文閱讀與書寫(二)": 2,
        "英文(一)": 2,
        "英文(二)": 2,
        "體育(一)": 1,
        "體育(二)": 1
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
        "會計學": 3
    },
    "系核心課程": {
        "組織管理學群": {
            "組織理論與管理": 3,
            "組織行為": 3
        },
        "公私決策學群": {
            "公共政策(一)": 2,
            "公共政策(二)": 2
        },
        "地區發展與行銷學群": {
            "行銷管理": 3,
            "消費者行為": 3
        }
    },
    "通識領域": {
        "文史哲藝術領域": {
            "美國文化": 2,
            "英文小品文賞析": 2
        },
        "社會脈動領域": {
            "法律素養": 2,
            "犯罪、法律與人權": 2
        },
        "生命科學領域": {
            "ESG與永續生活設計": 2,
            "水資源利用與保育": 2
        },
        "科技探索領域": {
            "AI人文藝術之應用": 2,
            "大數據分析概論": 2
        }
    },
    "自由選修": {}
}

# ================== 資料操作 ==================
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

# ================== 工具 ==================
def find_course(course_name):
    for cat, courses in course_structure.items():
        if cat == "通識領域":
            for domain, domain_courses in courses.items():
                if course_name in domain_courses:
                    return cat, course_name, domain_courses[course_name]
        elif cat == "系核心課程":
            for group, group_courses in courses.items():
                if course_name in group_courses:
                    return f"{cat} - {group}", course_name, group_courses[course_name]
        else:
            if course_name in courses:
                return cat, course_name, courses[course_name]
    return None, None, None

# ================== Streamlit App ==================
st.set_page_config(page_title="畢業學分檢查系統", layout="wide")
st.title("🎓 畢業學分檢查系統")

data = load_data()

menu = st.sidebar.radio("功能選擇", ["新增課程", "刪除課程", "已修課程列表", "畢業檢查"])

# ---------- 新增課程 ----------
if menu == "新增課程":
    st.subheader("➕ 新增課程")

    # 建立所有課程清單（剔除已修課程）
    all_courses = []
    for cat, courses in course_structure.items():
        if cat == "通識領域":
            for domain, domain_courses in courses.items():
                all_courses.extend(domain_courses.keys())
        elif cat == "系核心課程":
            for group, group_courses in courses.items():
                all_courses.extend(group_courses.keys())
        else:
            all_courses.extend(courses.keys())
    remaining_courses = [c for c in all_courses if c not in data["已修課程"]]

    if remaining_courses:
        course_name = st.selectbox("選擇課程", [""] + remaining_courses)
        if course_name:
            cat, cname, default_credit = find_course(course_name)
            domain_input = None
            if cat == "通識領域":
                domain_input = st.selectbox("通識領域", [""] + list(course_structure["通識領域"].keys()))
            credit_input = st.number_input(
                "學分（可自行修改）", min_value=1, step=1, value=default_credit
            )
            if st.button("新增"):
                data["已修課程"][cname] = {"學分": credit_input, "領域": domain_input if domain_input else None}
                save_data(data)
                st.success(f"✅ 已新增：{cname} ({credit_input}學分)，分類：{cat}")
    else:
        st.info("已經沒有可新增課程了！")

# ---------- 刪除課程 ----------
elif menu == "刪除課程":
    st.subheader("🗑 刪除課程")
    if data["已修課程"]:
        name = st.selectbox("選擇要刪除的課程", [""] + list(data["已修課程"].keys()))
        if st.button("刪除") and name:
            del data["已修課程"][name]
            save_data(data)
            st.success(f"🗑 已刪除課程：{name}")
    else:
        st.info("目前沒有已修課程可以刪除！")

# ---------- 已修課程列表 ----------
elif menu == "已修課程列表":
    st.subheader("📚 已修課程")
    if data["已修課程"]:
        for c, info in data["已修課程"].items():
            st.write(f"- {c} ({info['學分']} 學分) 領域：{info.get('領域','無')}")
    else:
        st.info("尚未加入課程")

# ---------- 畢業檢查 ----------
elif menu == "畢業檢查":
    st.subheader("📊 畢業檢查報告")
    total_credits = sum(info["學分"] for info in data["已修課程"].values())
    st.metric("已修總學分", total_credits)

    # 系核心學群檢查
    st.write("### 📚 系核心學群檢查")
    for group, courses in course_structure["系核心課程"].items():
        group_total = sum(info["學分"] for c, info in data["已修課程"].items() if c in courses)
        st.metric(group, f"{group_total} 學分", delta="需求 ≥ 6 學分")

    # 通識檢查
    st.write("### 🌍 通識領域檢查")
    for domain, domain_courses in course_structure["通識領域"].items():
        domain_total = sum(info["學分"] for c, info in data["已修課程"].items() if c in domain_courses)
        st.metric(domain, f"{domain_total} 學分", delta="需求 ≥ 2")
