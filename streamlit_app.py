def graduation_check():
    d = load_data()
    req = course_structure["總體要求"]
    results = []

    # 課程分類
    common_required = course_structure["課程"]["共同必修"]
    required_courses = course_structure["課程"]["系訂必修"]
    elective_courses = course_structure["課程"]["系內選修"]

    # 已修共同必修
    taken_common_courses = [c for c in common_required if c in d["已修課程"]]
    taken_common = sum(d["已修課程"][c]["學分"] for c in taken_common_courses)
    missing_common = [c for c in common_required if c not in d["已修課程"]]
    results.append(f"共同必修：已修 {len(taken_common_courses)} / 9 門課，共 {taken_common} 學分")
    if missing_common:
        results.append("▶️ 還沒修的共同必修課程：" + "、".join(missing_common))

    # 已修系訂必修
    taken_required = sum(info["學分"] for c, info in d["已修課程"].items() if c in required_courses)
    missing_required = [c for c in required_courses if c not in d["已修課程"]]
    results.append(f"系訂必修：已修 {taken_required} / {req['系訂必修學分']} 學分")
    if missing_required:
        results.append("▶️ 還沒修的系訂必修課程：" + "、".join(missing_required))

    # 系內選修
    taken_elective = sum(info["學分"] for c, info in d["已修課程"].items() if c in elective_courses)
    free_elective = sum(info["學分"] for c, info in d["已修課程"].items()
                        if c not in elective_courses and c not in required_courses and c not in common_required and not (info.get("領域","").startswith("A")))
    total_elective = taken_elective + free_elective
    results.append(f"系內/自由選修：已修 {total_elective} / {req['總選修學分']} 學分")
    if taken_elective < req["系內選修最低學分"]:
        results.append(f"⭐️ 還要修 {req['系內選修最低學分'] - taken_elective} 學分的系內選修！")
    if total_elective < req["總選修學分"]:
        results.append(f"⭐️ 還要修 {req['總選修學分'] - total_elective} 學分的選修！")

    # 通識學分與國文抵扣
    ge_total = 0
    ge_domains = set()
    for c, info in d["已修課程"].items():
        domain = info.get("領域")
        if domain and domain.startswith("A"):
            ge_total += info["學分"]
            ge_domains.add(domain)

    chinese_credit = 0
    if "國文上" in d["已修課程"]:
        chinese_credit += 3
    if "國文下" in d["已修課程"]:
        chinese_credit += 3

    deductible = 0
    for dom in ["A1","A2","A3","A4"]:
        for c, info in d["已修課程"].items():
            if info.get("領域")==dom:
                deductible = min(chinese_credit,3)
                break

    actual_ge = max(ge_total - deductible,0)
    results.append(f"通識：已修 {actual_ge} / {req['通識學分']} 學分，涵蓋領域數 {len(ge_domains)} / {req['通識至少領域數']}")
    if actual_ge < req["通識學分"]:
        results.append(f"⭐️ 通識還差 {req['通識學分'] - actual_ge} 學分")

    # 總畢業學分（包含共同必修 + 通識 + 系訂必修 + 選修）
    total_credits = taken_common + actual_ge + taken_required + total_elective
    results.insert(0, f"總畢業學分：{total_credits} / {req['畢業總學分']}")

    return results
