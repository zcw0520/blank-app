import streamlit as st
import json
import os

DATA_FILE = "courses_data.json"

# ---------- 行政管理系完整課程表 ----------
COURSE_STRUCTURE = {
    "校核心必修": {
        "中文閱讀與書寫(一)":2, "中文閱讀與書寫(二)":2,
        "英文(一)":2, "英文(二)":2,
        "體育(一)":1, "體育(二)":1
    },
    "院核心必修": {
        "組織與社會":2, "運算思維與程式設計":2
    },
    "系基礎必修": {
        "政治學":3, "行政學":3, "經濟學":3, "法學緒論":3,
        "中華民國憲法與政府":3, "管理學":3, "統計學":3,
        "社會科學研究法":3, "專題與實習":3
    },
    "系基礎選修": {
        "企業概論":3, "社會學":3, "會計學":3, "應用統計學":3,
        "行政管理理論":2, "政治經濟學":3, "行政法(一)":2,
        "民法(一)":2, "行政法(二)":2, "民法(二)":2,
        "財政學":3, "公共經濟學":3, "刑法":3, "第三部門":2,
        "專門議題研究":2, "國際關係":2, "專業英文":2
    },
    "組織管理學群": {
        "組織理論與管理":3, "公共管理":2,
        "組織行為":3, "人力資源管理":3
    },
    "公私決策學群": {
        "公共政策(一)":2, "公共政策(二)":2
    },
    "地區發展與行銷學群": {
        "行銷管理":3
    },
    "通識文史哲藝術": {
        "美國文化":2, "英文小品文賞析":2
    },
    "通識社會脈動": {
        "法律素養":2, "犯罪、法律與人權":2
    },
    "通識生命科學": {
        "ESG與永續生活設計":2
    },
    "通識科技探索": {
        "AI人文藝術之應用":2
    },
    "自由選修": {}
}

# ---------- 讀取/儲存 ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return {"已修課程":{}}

def save_data(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=4)

data = load_data()

# ---------- 自動歸類 ----------
def categorize_course(name):
    for cat, courses in COURSE_STRUCTURE.items():
        if name in courses:
            return cat, courses[name]
    # 不在已知課表 -> 判斷自由選修
    return "自由選修", 0

# ---------- 計算 ----------
def total_credits():
    return sum(c["學分"] for c in data["已修課程"].values())

def credits_in_category(category):
    return sum(c["學分"] for c in data["已修課程"].values() if c["類別"]==category)

def check_general_ed():
    domains = ["通識文史哲藝術","通識社會脈動","通識生命科學","通識科技探索"]
    domain_credits = {d:0 for d in domains}
    for c, info in data["已修課程"].items():
        if info["類別"].startswith("通識"):
            domain_credits[info["類別"]]+=info["學分"]
    total = sum(domain_credits.values())
    domain_count = sum(1 for v in domain_credits.values() if v>0)
    return total, domain_count, domain_credits

# ---------- Streamlit ----------
st.title("行政管理系課程登錄與畢業檢查")

menu = st.sidebar.selectbox("選單", ["新增課程","刪除課程","已修課程列表","總學分","畢業檢查"])

# ---------- 新增課程 ----------
if menu=="新增課程":
    course_name = st.text_input("課程名稱")
    course_credit = st.number_input("學分(如未知可先填0)", min_value=0, max_value=10, value=0, step=1)
    if st.button("新增課程"):
        cat, default_credit = categorize_course(course_name)
        credit = course_credit if course_credit>0 else default_credit
        data["已修課程"][course_name]={"學分":credit,"類別":cat}
        save_data(data)
        st.success(f"已新增課程：{course_name} ({credit} 學分) 類別：{cat}")

# ---------- 刪除 ----------
elif menu=="刪除課程":
    courses = list(data["已修課程"].keys())
    to_delete = st.multiselect("選擇要刪除的課程", courses)
    if st.button("刪除"):
        for c in to_delete:
            data["已修課程"].pop(c)
        save_data(data)
        st.success(f"已刪除 {len(to_delete)} 門課程")

# ---------- 已修課程 ----------
elif menu=="已修課程列表":
    st.subheader("已修課程")
    if not data["已修課程"]:
        st.write("尚未登錄任何課程")
    else:
        for c, info in data["已修課程"].items():
            st.write(f"- {c} ({info['學分']} 學分) 類別：{info['類別']}")

# ---------- 總學分 ----------
elif menu=="總學分":
    st.write(f"目前總學分： {total_credits()}")

# ---------- 畢業檢查 ----------
elif menu=="畢業檢查":
    st.subheader("畢業條件檢查")
    if not data["已修課程"]:
        st.write("尚未登錄任何課程")
    else:
        tot = total_credits()
        st.write(f"總學分：{tot}/132")

        school_core = credits_in_category("校核心必修")
        st.write(f"校核心必修：{school_core}/10")

        院_core = credits_in_category("院核心必修")
        st.write(f"院核心必修：{院_core}/4")

        sys_base_req = credits_in_category("系基礎必修")
        sys_base_ele = credits_in_category("系基礎選修")
        st.write(f"系基礎必修：{sys_base_req}/27；系選修：{sys_base_ele}/23")

        group1 = credits_in_category("組織管理學群")
        group2 = credits_in_category("公私決策學群")
        group3 = credits_in_category("地區發展與行銷學群")
        st.write(f"組織管理學群：{group1}/10")
        st.write(f"公私決策學群：{group2}/10")
        st.write(f"地區發展與行銷學群：{group3}/10")

        ge_total, ge_domains, domain_credits = check_general_ed()
        st.write(f"通識選修已修 {ge_total}/18 學分，涵蓋 {ge_domains} 個領域")
        for d, c in domain_credits.items():
            st.write(f"- {d}: {c} 學分")

        free_cr = credits_in_category("自由選修")
        st.write(f"自由選修：{free_cr}/20")

        professional = sum([credits_in_category(cat) for cat in ["院核心必修","系基礎必修","系基礎選修","組織管理學群","公私決策學群","地區發展與行銷學群"]])
        st.write(f"專業課程總學分：{professional}/80")

        ok = (tot>=132 and school_core>=10 and 院_core>=4 and sys_base_req>=27 and sys_base_ele>=23 and
              group1>=10 and group2>=10 and group3>=10 and ge_total>=18 and ge_domains>=3 and free_cr>=20 and professional>=80)
        st.write("➡️ 畢業條件整體檢查：", "✅ 已達成" if ok else "⚠️ 尚未達成")
