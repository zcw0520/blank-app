import streamlit as st
import json
import os

# ---------- 資料檔 ----------
DATA_FILE = "courses_data.json"

# ---------- 讀取/儲存 ----------
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
    return sum(c["學分"] for c in data["已修課程"].values())

def category_credits(cat_name):
    return sum(c["學分"] for c in data["已修課程"].values() if c["類別"] == cat_name)

# ---------- Streamlit GUI ----------
st.title("可自訂課程與畢業檢查系統")

menu = st.sidebar.selectbox("選單", [
    "新增課程", "刪除課程", "已修課程列表", "總學分", "畢業檢查"
])

# ---------- 新增課程 ----------
if menu == "新增課程":
    course_name = st.text_input("課程名稱")
    course_credit = st.number_input("學分", min_value=1, max_value=10, value=2, step=1)
    course_category = st.text_input("類別 (如: 通識、自由選修、院核心...)")
    if st.button("新增課程"):
        if not course_name or not course_category:
            st.warning("請輸入課程名稱和類別")
        else:
            data["已修課程"][course_name] = {
                "學分": course_credit,
                "類別": course_category
            }
            save_data(data)
            st.success(f"已新增課程：{course_name} ({course_credit} 學分) 類別：{course_category}")

# ---------- 刪除課程 ----------
elif menu == "刪除課程":
    courses = list(data["已修課程"].keys())
    to_delete = st.multiselect("選擇要刪除的課程", courses)
    if st.button("刪除"):
        for c in to_delete:
            data["已修課程"].pop(c)
        save_data(data)
        st.success(f"已刪除 {len(to_delete)} 門課程")

# ---------- 已修課程列表 ----------
elif menu == "已修課程列表":
    st.subheader("已修課程")
    if not data["已修課程"]:
        st.write("尚未登錄任何課程")
    else:
        for c, info in data["已修課程"].items():
            st.write(f"- {c} ({info['學分']} 學分) 類別：{info['類別']}")

# ---------- 總學分 ----------
elif menu == "總學分":
    st.write(f"總學分： {total_credits()}")

# ---------- 畢業檢查 ----------
elif menu == "畢業檢查":
    st.subheader("畢業條件檢查")
    if not data["已修課程"]:
        st.write("尚未登錄任何課程")
    else:
        st.write(f"總學分： {total_credits()}")
        # 統計每個類別學分
        categories = {}
        for c in data["已修課程"].values():
            cat = c["類別"]
            categories[cat] = categories.get(cat, 0) + c["學分"]

        st.write("各類別學分：")
        for cat, cr in categories.items():
            st.write(f"- {cat}: {cr} 學分")

        # 假設畢業門檻設定
        graduation_req = {
            "院核心": 10,
            "系必修": 40,
            "自由選修": 20,
            "通識": 30
        }
        st.write("畢業檢查狀態：")
        for cat, req in graduation_req.items():
            earned = categories.get(cat, 0)
            if earned >= req:
                st.success(f"{cat} 已達標 ({earned}/{req} 學分)")
            else:
                st.warning(f"{cat} 尚缺 {req-earned} 學分 ({earned}/{req})")
