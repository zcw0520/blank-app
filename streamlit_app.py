import json
import os
import difflib
import streamlit as st

DATA_FILE = "default_course_structure"
EXTERNAL_COURSES_FILE = "my_courses.json"

# ================== 課程結構 ==================
default_course_structure = {
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
        "會計學": 3,
        "應用統計學": 3,
        "行政管理理論": 2,
        "政治經濟學": 3,
        "行政法(一)": 2,
        "民法(一)": 2,
        "行政法(二)": 2,
        "民法(二)": 2,
        "財政學": 3,
        "公共經濟學": 3,
        "刑法": 3,
        "第三部門": 2,
        "專門議題研究": 2,
        "國際關係": 2,
        "專業英文": 2
    },
    "組織管理學群": {
        "組織理論與管理": 3,
        "公共管理": 2,
        "組織行為": 3,
        "人力資源管理": 3,
        "比較政府與政治": 2,
        "人力資源與組織發展": 3,
        "績效與薪酬管理": 3,
        "人事行政": 3,
        "政策與正義": 2,
        "電子治理": 2,
        "管理行政實務": 2
    },
    "公私決策學群": {
        "公共政策(一)": 2,
        "公共政策(二)": 2,
        "兩岸關係": 2,
        "創意與創新管理": 2,
        "政策規劃": 2,
        "問題分析與決策": 2,
        "民意調查": 2,
        "策略規劃與管理": 3,
        "政策執行與評估": 2,
        "決策與判斷分析": 2,
        "危機管理": 2,
        "公共事務管理個案分析": 2
    },
    "地區發展與行銷學群": {
        "行銷管理": 3,
        "消費者行為": 3,
        "都市與地方治理": 3,
        "文化產業行銷": 2,
        "服務行銷": 3,
        "政府談判": 3,
        "政治管理": 2,
        "地區經營管理": 2,
        "地方發展與地區行銷": 2,
        "廣告媒體": 3,
        "政策行銷": 3,
        "跨域管理": 2,
        "公益創投與社會行銷": 3
    },
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

# ================== 資料存取 ==================
def load_course_structure():
    if os.path.exists(EXTERNAL_COURSES_FILE):
        try:
            with open(EXTERNAL_COURSES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default_course_structure

course_structure = load_course_structure()

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
        if course_name in courses:
            return cat, course_name, courses[course_name]
    all_names = []
    for cat, courses in course_structure.items():
        all_names += list(courses.keys())
    matches = difflib.get_close_matches(course_name, all_names, n=3, cutoff=0.6)
    if matches:
        best = matches[0]
        for cat, courses in course_structure.items():
            if best in courses:
                return cat, best, courses[best]
    return None, None, None

def total_credits():
    data = load_data()
    return sum(data["已修課程"].values())

def check_three_core_groups():
    data = load_data()
    taken = data["已修課程"]
    result = {}
    for group in ["組織管理學群", "公私決策學群", "地區發展與行銷學群"]:
        total = 0
        for c, cr in taken.items():
            if c in course_structure.get(group, {}):
                total += cr
        result[group] = total
    return result

def check_general_ed():
    data = load_data()
    taken = data["已修課程"]
    domains = ["文史哲藝術領域", "社會脈動領域", "生命科學領域", "科技探索領域"]
    domain_credits = {d: 0 for d in domains}
    for c, cr in taken.items():
        for d in domains:
            if c in course_structure.get(d, {}):
                domain_credits[d] += cr
    return domain_credits

# ================== Streamlit App ==================
st.set_page_config(page_title="畢業學分檢查系統", layout="wide")
st.title("🎓 畢業學分檢查系統")

data = load_data()

# === 功能選單 ===
tab1, tab2 = st.tabs(["➕ 加入課程", "📊 畢業檢查"])

with tab1:
    st.subheader("新增已修課程")
    course_input = st.text_input("課程名稱")
    if st.button("加入"):
        if course_input:
            cat, cname, credit = find_course(course_input)
            if cname:
                data["已修課程"][cname] = credit
                save_data(data)
                st.success(f"✅ 已加入 {cname} ({credit}學分)")
            else:
                st.error("❌ 找不到課程，請確認名稱")

    if st.button("清除所有已修課程"):
        save_data({"已修課程": {}})
        st.warning("⚠️ 已清空資料")

    st.subheader("📖 已修課程列表")
    if data["已修課程"]:
        for c, cr in data["已修課程"].items():
            st.write(f"- {c} ({cr} 學分)")
    else:
        st.write("尚未加入課程")

with tab2:
    st.subheader("📊 畢業檢查報告")
    total = total_credits()
    st.metric("已修總學分", total)

    # 系核心學群
    st.write("### 📚 系核心學群檢查")
    three_groups = check_three_core_groups()
    cols = st.columns(3)
    for i, (g, cr) in enumerate(three_groups.items()):
        with cols[i]:
            st.metric(g, f"{cr} 學分", delta=f"需求 ≥ 6 學分")

    # 通識
    st.write("### 🌍 通識領域檢查")
    ge = check_general_ed()
    cols = st.columns(4)
    for i, (d, cr) in enumerate(ge.items()):
        with cols[i]:
            st.metric(d, f"{cr} 學分", delta="需求 ≥ 2 學分")

    st.write("⚠️ 系核心必修、選修與通識的最低學分需求可依學校規定修改。")
