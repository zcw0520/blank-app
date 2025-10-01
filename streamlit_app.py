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
        "經濟學": 3
    },
    "系核心課程": {
        "組織管理學群": {"組織理論與管理": 3},
        "公私決策學群": {"公共政策(一)": 2},
        "地區發展與行銷學群": {"行銷管理": 3}
    },
    "通識領域": {
        "文史哲藝術領域": {"美國文化": 2},
        "社會脈動領域": {"法律素養": 2},
        "生命科學領域": {"ESG與永續生活設計": 2},
        "科技探索領域": {"AI人文藝術之應用": 2}
    }
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
    # 先找結構裡有的課程
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
    # 找不到就當自由選修
    return "自由選修", course_name, 0

# ================== Streamlit App ==================
st.set_page_config(page_title="畢業學分檢查系統", layout="wide")
st.title("🎓 畢業學分檢查系統")

data = load_data()

menu = st.sidebar.radio("功能選擇", ["新增課程", "刪除課程", "已修課程列表", "畢業檢查"])

# ---------- 新增課程 ----------
if menu == "新增課程":
    st.subheader("➕ 新增課程（文字輸入）")

    course_input = st.text_input("輸入課程名稱")
    if course_input:
        cat, cname, default_credit = find_course(course_input)
        domain_input = None
        if cat == "通識領域":
            domain_input = st.selectbox("通識領域", [""] + list(course_structure["通識領域"].keys()))
        
        credit_input = st.number_input(
            "學分（可自行修改）", min_value=1, step=1, value=default_credit
        )

        if st.button("新增課程"):
            data["已修課程"][cname] = {"學分": credit_input, "領域": domain_input if domain_input else None, "分類": cat}
            save_data(data)
            st.success(f"✅ 已新增：{cname} ({credit_input}學分)，分類：{cat}")

# ---------- 刪除課程 ----------
elif menu == "刪除課程":
    st.subheader("🗑 刪除課程")
    if data["已修課程"]:
        name = st.text_input("輸入要刪除的課程名稱")
        if st.button("刪除") and name in data["已修課程"]:
            del data["已修課程"][name]
            save_data(data)
            st.success(f"🗑 已刪除課程：{name}")
        elif st.button("刪除") and name:
            st.warning("⚠️ 找不到課程")
    else:
        st.info("目前沒有已修課程可以刪除！")

# ---------- 已修課程列表 ----------
elif menu == "已修課程列表":
    st.subheader("📚 已修課程")
    if data["已修課程"]:
        for c, info in data["已修課程"].items():
            st.write(f"- {c} ({info['學分']} 學分) 分類：{info.get('分類','自由')}，領域：{info.get('領域','無')}")
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

    # 自由選修學分
    free_total = sum(info["學分"] for c, info in data["已修課程"].items() if info["分類"] == "自由選修")
    st.metric("自由選修", free_total)
