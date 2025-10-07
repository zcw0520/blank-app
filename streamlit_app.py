# app.py
import streamlit as st
import json
import os

DATA_FILE = "my_courses.json"

# =========================
# 完整課程架構（行政管理學系版）
# （取自你提供的 default_course_structure，已包含各類別與學分）
# =========================
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
    # 通識四大領域
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

# =========================
# Helper: load / save
# =========================
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"已修課程": {}}
    return {"已修課程": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# =========================
# Graduation check logic (adapted from your CLI)
# Returns markdown text
# =========================
def graduation_check_text(taken_dict):
    # taken_dict: {course_name: credit}
    def in_group(course, group):
        return course in course_structure.get(group, {})

    tot = sum(taken_dict.values())
    lines = []
    lines.append("## 🧾 畢業條件檢查報告")
    lines.append(f"- 目前總學分： **{tot} / 132**")

    # 校核心
    school_core_taken = sum(cr for c, cr in taken_dict.items() if in_group(c, "校核心必修"))
    lines.append(f"- 校核心必修：已修 **{school_core_taken} / 10** 學分")

    # 院核心
   院_core_taken = sum(cr for c, cr in taken_dict.items() if in_group(c, "院核心必修"))
    lines.append(f"- 院核心必修：已修 **{院_core_taken} / 4** 學分")

    # 系基礎
    base_required_taken = sum(cr for c, cr in taken_dict.items() if in_group(c, "系基礎必修"))
    base_elective_taken = sum(cr for c, cr in taken_dict.items() if in_group(c, "系基礎選修"))
    lines.append(f"- 系基礎必修：已修 **{base_required_taken} / 27**")
    lines.append(f"- 系基礎選修：已修 **{base_elective_taken} / 23**")

    if base_required_taken < 27:
        lines.append(f"  - ⚠️ 系基礎必修尚差 **{27 - base_required_taken}** 學分")
    if base_elective_taken < 23:
        lines.append(f"  - ⚠️ 系基礎選修尚差 **{23 - base_elective_taken}** 學分")

    # 三大學群各 10學分
    core_groups = ["組織管理學群", "公私決策學群", "地區發展與行銷學群"]
    professional = 0
    core_group_lines = []
    for g in core_groups:
        v = sum(cr for c, cr in taken_dict.items() if in_group(c, g))
        core_group_lines.append(f"- {g}：已修 **{v} / 10** 學分" + (f"  ⚠️ 尚差 **{10-v}**" if v < 10 else "  ✅ 達標"))
        professional += v

    lines.extend(core_group_lines)

    # 通識檢查
    domains = ["文史哲藝術領域", "社會脈動領域", "生命科學領域", "科技探索領域"]
    domain_credits = {d: 0 for d in domains}
    for c, cr in taken_dict.items():
        for d in domains:
            if in_group(c, d):
                domain_credits[d] += cr
        if in_group(c, "通識不分領域"):
            domain_credits["文史哲藝術領域"] += cr  # 歸入文史哲
    ge_total = sum(domain_credits.values())
    domain_count = sum(1 for v in domain_credits.values() if v > 0)
    lines.append(f"- 通識選修（四大領域）：已修 **{ge_total}** 學分，涵蓋 **{domain_count}** 個領域（需 18 學分 & 至少 3 個領域）")
    for d, c in domain_credits.items():
        lines.append(f"  - {d}: {c} 學分")

    # 自由選修
    free_taken = sum(cr for c, cr in taken_dict.items() if c in course_structure.get("自由選修", {}))
    # plus any course not in any category count as '其他' -> consider as 自由選修
    others = [c for c in taken_dict.keys() if not any(in_group(c, g) for g in course_structure.keys())]
    other_credits = sum(taken_dict[c] for c in others)
    free_total = free_taken + other_credits
    lines.append(f"- 自由選修：已修 **{free_total} / 20** 學分")

    # 專業相關（院核心 + 系基礎 + 三大學群）
    professional_total = 0
    for c, cr in taken_dict.items():
        for group in ["院核心必修", "系基礎必修", "系基礎選修", "組織管理學群", "公私決策學群", "地區發展與行銷學群"]:
            if in_group(c, group):
                professional_total += cr
                break
    lines.append(f"- 專業相關學分（估）：**{professional_total} / 80**")

    # final decision
    ok = True
    if tot < 132: ok = False
    if school_core_taken < 10: ok = False
    if 院_core_taken < 4: ok = False
    if base_required_taken < 27 or base_elective_taken < 23: ok = False
    if any(sum(cr for c, cr in taken_dict.items() if in_group(c, g)) < 10 for g in core_groups): ok = False
    if ge_total < 18 or domain_count < 3: ok = False
    if free_total < 20: ok = False
    if professional_total < 80: ok = False

    if ok:
        lines.append("\n➡️ **整體判定：✅ 看起來已達成全部條件（以教務系統為準）**")
    else:
        lines.append("\n➡️ **整體判定：⚠️ 尚未全部達成（請見上方差距）**")

    return "\n".join(lines)

# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="行政管理系 課程管理", layout="wide")
st.title("🎓 行政管理學系 - 完整課程輸入與畢業檢查")

# load saved data
data = load_data()
taken_saved = data.get("已修課程", {})

# We'll keep a working dict new_taken while user edits
if "new_taken" not in st.session_state:
    st.session_state.new_taken = dict(taken_saved)

# Helper to save st.session_state.new_taken to file
def persist():
    save_data({"已修課程": st.session_state.new_taken})
    st.success("已儲存到 my_courses.json")

# Sidebar: quick stats & actions
with st.sidebar:
    st.header("🔧 快速操作")
    if st.button("儲存目前資料"):
        persist()
    if st.button("重新載入已存資料"):
        data2 = load_data()
        st.session_state.new_taken = dict(data2.get("已修課程", {}))
        st.experimental_rerun()
    st.download_button("下載 my_courses.json",
                       json.dumps({"已修課程": st.session_state.new_taken}, ensure_ascii=False, indent=4),
                       file_name="my_courses.json",
                       mime="application/json")
    st.markdown("---")
    total_now = sum(st.session_state.new_taken.values())
    st.metric("目前總學分", f"{total_now} / 132")
    st.markdown("說明：此畫面可同時輸入所有類別（校核心 / 院核心 / 系基礎 / 系選修 / 三大學群 / 通識 / 自由選修）。")

# --- Functions to render category editor ---
def render_category(cat_name):
    st.subheader(cat_name)
    # init rows state for each category
    key_rows = f"rows_{cat_name}"
    if key_rows not in st.session_state:
        # initialize with one empty row (index 0)
        st.session_state[key_rows] = [{"course": "–"}]

    cols = st.columns([3, 1, 1])
    with cols[0]:
        if st.button(f"➕ 新增 {cat_name} 列", key=f"add_{cat_name}"):
            st.session_state[key_rows].append({"course": "–"})
    with cols[1]:
        if st.button(f"🗑️ 清空 {cat_name}", key=f"clear_{cat_name}"):
            # remove all entries of this category from new_taken
            for c in list(st.session_state.new_taken.keys()):
                if c in course_structure.get(cat_name, {}):
                    del st.session_state.new_taken[c]
            st.session_state[key_rows] = [{"course": "–"}]
            st.experimental_rerun()
    with cols[2]:
        if st.button(f"刪除最後一列 ({cat_name})", key=f"pop_{cat_name}"):
            if len(st.session_state[key_rows]) > 1:
                st.session_state[key_rows].pop()

    # render each row
    for i, row in enumerate(st.session_state[key_rows]):
        c1, c2 = st.columns([4, 1])
        with c1:
            choices = ["–"] + list(course_structure.get(cat_name, {}).keys())
            sel = st.selectbox(f"{cat_name} - 選課 ({i+1})", choices, index=choices.index(row.get("course", "–")) if row.get("course", "–") in choices else 0, key=f"{cat_name}_course_{i}")
        with c2:
            credit_display = ""
            if sel != "–":
                credit_display = course_structure[cat_name][sel]
                st.write(f"📘 {credit_display} 學分")
            else:
                st.write("")
        # update taken
        if sel != "–":
            st.session_state.new_taken[sel] = course_structure[cat_name][sel]
        else:
            # if previously had course in this row, attempt to remove
            prev = row.get("course")
            if prev and prev in st.session_state.new_taken and prev in course_structure.get(cat_name, {}):
                del st.session_state.new_taken[prev]
        # store back the selected course for persistence in session_state
        st.session_state[key_rows][i]["course"] = sel

# ========== Render all categories ==========
# top-level categories order (你要的全部出現在畫面上)
categories_to_show = [
    "校核心必修",
    "院核心必修",
    "系基礎必修",
    "系基礎選修",
    "組織管理學群",
    "公私決策學群",
    "地區發展與行銷學群",
    "文史哲藝術領域",
    "社會脈動領域",
    "生命科學領域",
    "科技探索領域",
    "通識不分領域"
]

for cat in categories_to_show:
    render_category(cat)
    st.markdown("---")

# ===== 自由選修（可手動輸入課名+學分） =====
st.subheader("📝 自由選修（可輸入課名與學分）")
if "free_rows" not in st.session_state:
    st.session_state.free_rows = [{"name": "", "credit": 0}]

c1, c2 = st.columns([3, 1])
with c1:
    if st.button("➕ 新增自由選修列"):
        st.session_state.free_rows.append({"name": "", "credit": 0})
with c2:
    if st.button("🗑️ 清空所有自由選修"):
        # remove all non-structured courses from new_taken
        # (structured = any course present in course_structure categories)
        for c in list(st.session_state.new_taken.keys()):
            found = False
            for g in course_structure.keys():
                if c in course_structure[g]:
                    found = True
                    break
            if not found:
                del st.session_state.new_taken[c]
        st.session_state.free_rows = [{"name": "", "credit": 0}]
        st.experimental_rerun()

for i, row in enumerate(st.session_state.free_rows):
    cols = st.columns([3, 1, 1])
    with cols[0]:
        name = st.text_input(f"自由選修 課名 ({i+1})", value=row.get("name", ""), key=f"free_name_{i}")
    with cols[1]:
        credit = st.number_input(f"學分 ({i+1})", min_value=0, max_value=10, step=1, value=int(row.get("credit", 0)), key=f"free_credit_{i}")
    with cols[2]:
        if st.button(f"刪除此列 ({i+1})", key=f"free_del_{i}"):
            # remove course if exists
            if name.strip() in st.session_state.new_taken:
                del st.session_state.new_taken[name.strip()]
            st.session_state.free_rows.pop(i)
            st.experimental_rerun()
    # store into new_taken if name provided
    if name.strip():
        st.session_state.new_taken[name.strip()] = int(credit)
    st.session_state.free_rows[i]["name"] = name
    st.session_state.free_rows[i]["credit"] = int(credit)

# ===== 顯示 summary 與 存檔按鈕 =====
st.markdown("---")
col_a, col_b = st.columns([2, 1])
with col_a:
    st.subheader("📈 目前已登錄的課程（預覽）")
    if st.session_state.new_taken:
        for c, cr in sorted(st.session_state.new_taken.items()):
            # find category label if available
            cat_label = None
            for g, courses in course_structure.items():
                if c in courses:
                    cat_label = g
                    break
            label = cat_label if cat_label else "（自由/其他）"
            st.write(f"- {c} — {cr} 學分    {label}")
    else:
        st.write("目前尚未登錄任何課程。")

with col_b:
    st.subheader("操作")
    if st.button("💾 儲存並寫入 my_courses.json"):
        persist()
    if st.button("🔁 重新載入已存資料 (重新啟動畫面)"):
        st.session_state.new_taken = dict(load_data().get("已修課程", {}))
        st.experimental_rerun()

# ===== 畢業檢查（整合） =====
st.markdown("---")
st.subheader("🎓 畢業條件檢查")
if st.button("執行完整畢業檢查"):
    report_md = graduation_check_text(st.session_state.new_taken)
    st.markdown(report_md)
    st.stop()
else:
    st.write("按「執行完整畢業檢查」以顯示詳細報告。")

# Footer: quick totals
st.markdown("---")
tot = sum(st.session_state.new_taken.values())
st.write(f"**目前總學分： {tot} / 132**  （自動計算）")
