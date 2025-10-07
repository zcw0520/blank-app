import streamlit as st
import json
import os

# ---------- 設定檔 ----------
DATA_FILE = "my_courses.json"
COURSES_FILE = "courses.json"  # 你的完整課程表 JSON

# ---------- 讀取課程結構 ----------
if os.path.exists(COURSES_FILE):
    with open(COURSES_FILE, "r", encoding="utf-8") as f:
        course_structure = json.load(f)
else:
    st.error("找不到 courses.json，請放置完整課程表")
    st.stop()

# ---------- 讀取/儲存已修課 ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"已修課程": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# ---------- 工具函數 ----------
def total_credits():
    return sum(data["已修課程"].values())

def credits_by_category():
    cat_credits = {k: 0 for k in course_structure.keys()}
    cat_credits["其他"] = 0
    for c, cr in data["已修課程"].items():
        found = False
        for cat, courses in course_structure.items():
            if c in courses:
                cat_credits[cat] += cr
                found = True
                break
        if not found:
            cat_credits["其他"] += cr
    return cat_credits

def in_group(course, group):
    return course in course_structure.get(group, {})

def graduation_check():
    st.subheader("畢業條件檢查")
    taken = data["已修課程"]

    tot = total_credits()
    st.write(f"總學分： {tot} / 132")

    # 校核心
    school_core_taken = sum(cr for c, cr in taken.items() if in_group(c, "校核心必修"))
    st.write(f"校核心必修：{school_core_taken} / 10 學分")

    # 院核心
    院_core_taken = sum(cr for c, cr in taken.items() if in_group(c, "院核心必修"))
    st.write(f"院核心必修：{院_core_taken} / 4 學分")

    # 系基礎必修與選修
    base_required_taken = sum(cr for c, cr in taken.items() if in_group(c, "系基礎必修"))
    base_elective_taken = sum(cr for c, cr in taken.items() if in_group(c, "系基礎選修"))
    st.write(f"系基礎：必修 {base_required_taken}/27，選修 {base_elective_taken}/23，合計 {base_required_taken+base_elective_taken}/50")

    # 三大學群
    core_groups = ["組織管理學群", "公私決策學群", "地區發展與行銷學群"]
    for g in core_groups:
        v = sum(cr for c, cr in taken.items() if in_group(c, g))
        st.write(f"{g}：已修 {v}/10 學分")

    # 通識
    domains = ["文史哲藝術領域", "社會脈動領域", "生命科學領域", "科技探索領域"]
    domain_credits = {d: 0 for d in domains}
    for c, cr in taken.items():
        for d in domains:
            if in_group(c, d):
                domain_credits[d] += cr
        # 不分領域算到文史哲
        if in_group(c, "通識不分領域"):
            domain_credits["文史哲藝術領域"] += cr
    total_ge = sum(domain_credits.values())
    domain_count = sum(1 for v in domain_credits.values() if v > 0)
    st.write(f"通識選修已修 {total_ge} 學分，涵蓋 {domain_count} 個領域")
    for d, c in domain_credits.items():
        st.write(f"- {d}: {c} 學分")

    # 自由選修
    free_taken = sum(cr for c, cr in taken.items() if in_group(c, "自由選修"))
    st.write(f"自由選修：{free_taken} / 20 學分")

# ---------- Streamlit GUI ----------
st.title("行政管理學系課程系統")

menu = st.sidebar.selectbox("選單", [
    "新增通識課程", "新增自由選修", "刪除已修課程",
    "已修課程列表", "總學分", "畢業條件檢查"
])

# ---------- 新增通識課程 ----------
if menu == "新增通識課程":
    category = st.selectbox("選擇通識領域", 
                            ["文史哲藝術領域", "社會脈動領域", "生命科學領域", "科技探索領域", "通識不分領域"])
    courses_in_cat = course_structure.get(category, {})
    selected_courses = st.multiselect("選擇課程", list(courses_in_cat.keys()))
    if st.button("加入已修課程"):
        for c in selected_courses:
            data["已修課程"][c] = courses_in_cat[c]
        save_data(data)
        st.success(f"已加入 {len(selected_courses)} 門課程！")

# ---------- 新增自由選修 ----------
elif menu == "新增自由選修":
    name = st.text_input("自由選修課程名稱")
    credit = st.number_input("學分數", min_value=1, max_value=10, value=2, step=1)
    if st.button("加入自由選修"):
        if name:
            data["已修課程"][name] = credit
            if "自由選修" not in course_structure:
                course_structure["自由選修"] = {}
            course_structure["自由選修"][name] = credit
            save_data(data)
            st.success(f"已加入自由選修課程：{name} ({credit} 學分)")

# ---------- 刪除課程 ----------
elif menu == "刪除已修課程":
    taken_list = list(data["已修課程"].keys())
    to_delete = st.multiselect("選擇要刪除的課程", taken_list)
    if st.button("刪除課程"):
        for c in to_delete:
            data["已修課程"].pop(c, None)
        save_data(data)
        st.success(f"已刪除 {len(to_delete)} 門課程")

# ---------- 已修課程列表 ----------
elif menu == "已修課程列表":
    st.subheader("已修課程")
    if not data["已修課程"]:
        st.write("目前尚未登錄任何課程")
    else:
        for c, cr in data["已修課程"].items():
            st.write(f"- {c} ({cr} 學分)")

# ---------- 總學分 ----------
elif menu == "總學分":
    st.subheader("總學分")
    st.write(f"目前總學分： {total_credits()}")

# ---------- 畢業檢查 ----------
elif menu == "畢業條件檢查":
    graduation_check()
