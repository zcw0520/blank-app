import json
import os
import streamlit as st
import plotly.graph_objects as go

# ========== 課程結構 ==========
course_structure = {
    "總體要求": {
        "畢業總學分": 132,
        "校核心學分": 10,
        "院核心學分": 4,
        "系基礎必修": 27,
        "系基礎選修": 23,
        "系核心三群各10": 10,
        "自由選修": 20,
        "通識最低學分": 12,
        "通識至少領域數": 3
    },
    "課程": {
        "校核心必修": {
            "國文上": 2, "國文下": 2, "英文一": 2, "英文二": 2, "體育一": 1, "體育二": 1
        },
        "院核心必修": {
            "組織與社會": 2, "運算思維與程式設計": 2
        },
        "系基礎必修": {
            "政治學": 3, "行政學": 3, "經濟學": 3, "法學緒論": 3, "中華民國憲法與政府": 3,
            "管理學": 3, "統計學": 3, "社會科學研究法": 3, "專題與實習": 3
        },
        "系基礎選修": {
            "企業概論": 3, "社會學": 3, "會計學": 3, "應用統計學": 3, "行政管理理論": 2,
            "政治經濟學": 3, "行政法(一)": 2, "民法(一)": 2, "行政法(二)": 2, "民法(二)": 2,
            "財政學": 3, "公共經濟學": 3, "刑法": 3, "第三部門": 2, "專門議題研究": 2,
            "國際關係": 2, "專業英文": 2
        },
        "系核心學群": {
            "組織管理學群": {"組織理論與管理": 3, "公共管理": 2, "組織行為": 3, "人力資源管理": 3},
            "公私決策學群": {"公共政策(一)": 2, "公共政策(二)": 2, "兩岸關係": 2, "創意與創新管理": 2},
            "地區發展與行銷學群": {"行銷管理": 3, "消費者行為": 3, "都市與地方治理": 3, "文化產業行銷": 2}
        },
        "通識課程": {
            "(A1)文學與藝術": {}, "(A2)歷史思維": {}, "(A3)世界文明": {},
            "(A4)哲學與道德思考": {}, "(A5)公民意識與社會分析": {}, "(A8)生命科學": {}
        }
    }
}

DATA_FILE = "my_courses.json"

# ========== 資料操作 ==========
def init_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"已修課程": {}}, f, ensure_ascii=False, indent=4)

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
            for dom, dom_courses in courses.items():
                if name in dom_courses:
                    return cat, name, dom_courses[name]
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
def graduation_summary():
    d = load_data()
    req = course_structure["總體要求"]

    # 計算各類學分
    common = sum(d["已修課程"][c]["學分"] for c in course_structure["課程"]["校核心必修"] if c in d["已修課程"])
    college_core = sum(d["已修課程"][c]["學分"] for c in course_structure["課程"]["院核心必修"] if c in d["已修課程"])
    dept_required = sum(d["已修課程"][c]["學分"] for c in course_structure["課程"]["系基礎必修"] if c in d["已修課程"])
    dept_elective = sum(d["已修課程"][c]["學分"] for c in course_structure["課程"]["系基礎選修"] if c in d["已修課程"])
    
    # 系核心學群
    core_groups = course_structure["課程"]["系核心學群"]
    core_done = 0
    for group, courses in core_groups.items():
        core_done += sum(d["已修課程"].get(c, {"學分":0})["學分"] for c in courses)

    # 自由選修
    all_known = set()
    for cat in course_structure["課程"]:
        for c in course_structure["課程"][cat]:
            if isinstance(course_structure["課程"][cat][c], dict):
                all_known.update(course_structure["課程"][cat][c].keys())
            else:
                all_known.add(c)
    free = sum(info["學分"] for c, info in d["已修課程"].items() if c not in all_known)

    # 通識
    ge_domains = course_structure["課程"]["通識課程"].keys()
    ge_done = {dom:0 for dom in ge_domains}
    for c, info in d["已修課程"].items():
        dom = info.get("領域")
        if dom in ge_domains:
            ge_done[dom] += info["學分"]

    total_credits = common + college_core + dept_required + dept_elective + core_done + free + sum(ge_done.values())

    summary = {
        "總學分": (total_credits, req["畢業總學分"]),
        "校核心必修": (common, req["校核心學分"]),
        "院核心必修": (college_core, req["院核心學分"]),
        "系基礎必修": (dept_required, req["系基礎必修"]),
        "系基礎選修": (dept_elective, req["系基礎選修"]),
        "系核心學群": (core_done, 3*req["系核心三群各10"]),
        "自由選修": (free, req["自由選修"]),
        "通識": (sum(ge_done.values()), req["通識最低學分"]),
        "通識領域": ge_done
    }
    return summary

# ========== Streamlit UI ==========
st.title("🎓 畢業學分檢查板")

menu = st.sidebar.radio("功能選擇", ["新增課程", "刪除課程", "已修課程列表", "畢業檢查"])

if menu == "新增課程":
    name = st.text_input("課程名稱")
    credit = st.number_input("學分（若課程已知可留 0）", min_value=0, max_value=10, value=0)
    ge_options = ["非通識"] + list(course_structure["課程"]["通識課程"].keys())
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
    st.subheader("📊 畢業進度可視化")
    summary = graduation_summary()

    # 總學分進度
    st.metric("總學分進度", f"{summary['總學分'][0]} / {summary['總學分'][1]}")

    # 主分類圓餅圖
    fig = go.Figure(go.Pie(
        labels=["校核心","院核心","系基礎必修","系基礎選修","系核心學群","自由選修","通識"],
        values=[summary["校核心必修"][0], summary["院核心必修"][0], summary["系基礎必修"][0],
                summary["系基礎選修"][0], summary["系核心學群"][0], summary["自由選修"][0], summary["通識"][0]],
        hole=0.4, textinfo='label+value'
    ))
    fig.update_layout(title="學分分類分布")
    st.plotly_chart(fig, use_container_width=True)

    # 通識領域圓餅圖
    fig2 = go.Figure(go.Pie(
        labels=list(summary["通識領域"].keys()),
        values=list(summary["通識領域"].values()),
        hole=0.4, textinfo='label+value'
    ))
    fig2.update_layout(title="通識各領域學分")
    st.plotly_chart(fig2, use_container_width=True)
