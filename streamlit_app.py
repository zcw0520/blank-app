import streamlit as st
import json
import os

DATA_FILE = "my_courses.json"

# ===== 課程架構（取自你的行政管理系版本） =====
default_course_structure = {
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
    "自由選修": {}
}

# ===== 儲存/載入功能 =====
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"已修課程": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ===== 主頁 =====
st.title("🎓 行政管理學系 通識與自由選修管理系統")

data = load_data()
taken = data["已修課程"]

st.header("📚 通識課程")
domains = ["–", "文史哲藝術領域", "社會脈動領域", "生命科學領域", "科技探索領域"]

# 用 session_state 記錄行數
if "ge_rows" not in st.session_state:
    st.session_state.ge_rows = [{"domain": "–", "course": "–"}]

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("➕ 增加通識課程列"):
        st.session_state.ge_rows.append({"domain": "–", "course": "–"})
with col2:
    if st.button("🗑️ 清空通識課程"):
        st.session_state.ge_rows = [{"domain": "–", "course": "–"}]
        # 清空資料
        for c in list(taken.keys()):
            if any(c in default_course_structure[d] for d in domains if d != "–"):
                del taken[c]
        save_data(data)
        st.experimental_rerun()

new_taken = {}

for i, row in enumerate(st.session_state.ge_rows):
    st.markdown(f"**第 {i+1} 列**")
    c1, c2, c3 = st.columns([2, 3, 1])
    with c1:
        domain = st.selectbox(
            "領域", domains, key=f"domain_{i}", index=domains.index(row["domain"])
        )
    with c2:
        course_list = ["–"]
        if domain != "–":
            course_list += list(default_course_structure[domain].keys())
        course = st.selectbox(
            "課程名稱", course_list, key=f"course_{i}", index=course_list.index(row["course"]) if row["course"] in course_list else 0
        )
    with c3:
        credit = 0
        if domain != "–" and course != "–":
            credit = default_course_structure[domain][course]
            st.write(f"📘 {credit} 學分")
        else:
            st.write("")

    # 更新已修課紀錄
    if domain != "–" and course != "–":
        new_taken[course] = credit

st.header("📝 自由選修")
if "free_rows" not in st.session_state:
    st.session_state.free_rows = [{"name": "", "credit": ""}]

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("➕ 增加自由選修列"):
        st.session_state.free_rows.append({"name": "", "credit": ""})
with col2:
    if st.button("🗑️ 清空自由選修"):
        st.session_state.free_rows = [{"name": "", "credit": ""}]
        for c in list(taken.keys()):
            if c not in sum([list(default_course_structure[d].keys()) for d in domains if d != "–"], []):
                del taken[c]
        save_data(data)
        st.experimental_rerun()

for i, row in enumerate(st.session_state.free_rows):
    c1, c2 = st.columns([3, 1])
    with c1:
        name = st.text_input("課程名稱", value=row["name"], key=f"free_name_{i}")
    with c2:
        credit = st.number_input("學分", min_value=0, max_value=10, step=1, value=int(row["credit"] or 0), key=f"free_credit_{i}")
    if name.strip():
        new_taken[name.strip()] = credit

# 更新資料並儲存
data["已修課程"] = new_taken
save_data(data)

# 顯示統計
st.subheader("📈 統計")
total = sum(new_taken.values())
st.write(f"**目前已修學分：{total} 學分**")

st.download_button(
    "💾 下載 my_courses.json",
    json.dumps(data, ensure_ascii=False, indent=4),
    "my_courses.json",
    mime="application/json"
)

# 匯入畢業條件檢查（簡化版：呼叫舊函式或外部整合）
if st.button("🎓 檢查畢業條件（完整報告）"):
    st.write("請在整合版 Python 程式中呼叫 `graduation_check()` 查看詳細報告。")
    st.write("（此介面僅管理通識與自由選修；完整檢查請執行主程式。）")
