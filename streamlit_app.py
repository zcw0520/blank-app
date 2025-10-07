import streamlit as st
import json
import os

# ---------- 資料檔 ----------
DATA_FILE = "my_courses.json"

# ---------- 內建完整課程結構 ----------
course_structure = {
    "文史哲藝術領域": {
        "美國文化": 2,
        "英文小品文賞析": 2,
        "英語口語表達技巧": 2,
        "旅遊英文": 2,
        "時事英文": 2,
        "英文口語表達技巧": 2,
        "職場英文": 2,
        "小說與社會關懷": 2,
        "文學與現代生活": 2,
        "臺灣經典文獻選讀": 2,
        "經典文學導讀": 2,
        "臺灣歷史與文化": 2,
        "影像藝術思維": 2,
        "攝影藝術": 2,
        "空間美學": 2,
        "音樂與人生": 2,
        "表演藝術欣賞": 2
    },
    "社會脈動領域": {
        "法律素養": 2,
        "犯罪、法律與人權": 2,
        "亞太地區地緣政治與中國": 2,
        "政治學概要": 2,
        "國際關係發展與理論": 2,
        "臺灣主權地位的國際觀": 2,
        "職場與法律": 2,
        "服務學習與社會關懷": 2,
        "理財規劃": 2,
        "管理學概論": 2,
        "領導藝術": 2
    },
    "生命科學領域": {
        "ESG與永續生活設計": 2,
        "水資源利用與保育": 2,
        "臺灣自然保育議題": 2,
        "海洋生命科學導論": 2,
        "生命教育": 2,
        "大學生的幸福學": 2,
        "生死學": 2,
        "生物科技的應用": 2,
        "運動與人生": 2,
        "運動的藝術與實踐": 2
    },
    "科技探索領域": {
        "AI人文藝術之應用": 2,
        "AI遇見設計思考": 2,
        "大數據分析概論": 2,
        "生成式AI之運用": 2,
        "計算機概論與 Python 程式設計": 2,
        "機器學習概論": 2,
        "機器人思維與設計": 2,
        "網路資料探勘與分析": 2,
        "網頁設計與網站建置概論": 2,
        "物聯網應用": 2,
        "行動裝置程式設計": 2
    },
    "通識不分領域": {
        "博雅教育講座": 2
    },
    "自由選修": {}
}

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

def in_group(course, group):
    return course in course_structure.get(group, {})

def graduation_check():
    st.subheader("畢業條件檢查")
    taken = data["已修課程"]

    tot = total_credits()
    st.write(f"總學分： {tot} / 132")

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
