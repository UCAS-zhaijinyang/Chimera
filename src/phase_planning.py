"""Business phases with variable durations; no week-based intermediate plan."""
import json
import math
import re

def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def build_phase_meetings(company):
    require(type(company["total_workdays"]) is int and company["total_workdays"] > 0, "invalid total workdays")
    require(type(company["hours_per_person_day"]) in (int, float)
            and 0 < company["hours_per_person_day"] <= 24, "invalid daily capacity")
    require(text(company["company_type"]) and text(company["goal"]), "missing company context")
    ids = [p["id"] for p in company["profiles"]]
    require(ids and len(ids) == len(set(ids)), "invalid employee roster")
    for p in company["profiles"]:
        require(all(text(p.get(k)) for k in ["id", "name", "role", "description", "personality"]), "invalid profile")
    departments = company["departments"]
    dept_ids = [d["id"] for d in departments]
    require(dept_ids and len(dept_ids) == len(set(dept_ids)), "invalid departments")
    require(all(re.fullmatch(r"[A-Za-z0-9_-]+", i) for i in ids + dept_ids), "unsafe ID")
    members = []
    for d in departments:
        require(d["member_ids"] and d["leader_id"] in d["member_ids"], "invalid leader")
        members.extend(d["member_ids"])
    require(len(members) == len(set(members)) and set(members) == set(ids), "employee coverage mismatch")
    return [{"id": "leadership", "member_ids": [d["leader_id"] for d in departments]}] + [
        {"id": "department_" + d["id"], "department_id": d["id"], "member_ids": d["member_ids"]}
        for d in departments]


def phase_ranges(plan):
    start, ranges = 1, {}
    for phase in plan["phases"]:
        duration = phase["duration_days"]
        require(type(duration) is int and duration > 0, "duration_days must be a positive integer")
        require(phase["phase_id"] not in ranges, "duplicate phase ID")
        ranges[phase["phase_id"]] = (start, start + duration - 1)
        start += duration
    return ranges


def validate_phase_plan(plan, company):
    require(isinstance(plan, dict) and plan["phases"], "missing phases")
    for p in plan["phases"]:
        require(all(text(p.get(k)) for k in ["phase_id", "name", "goal"]), "unnamed phase")
        require(re.fullmatch(r"[A-Za-z0-9_-]+", p["phase_id"]), "unsafe phase ID")
    ranges = phase_ranges(plan)
    require(sum(p["duration_days"] for p in plan["phases"]) == company["total_workdays"], "phase durations do not cover total workdays")
    departments = {d["id"] for d in company["departments"]}
    tasks = plan["department_tasks"]
    task_map = {t["task_id"]: t for t in tasks}
    require(len(task_map) == len(tasks) and all(text(i) for i in task_map), "invalid task IDs")
    for t in tasks:
        require(t["phase_id"] in ranges and t["department_id"] in departments and text(t["goal"]), "invalid department task")
    require({(t["department_id"], t["phase_id"]) for t in tasks} ==
            {(d, p) for d in departments for p in ranges}, "missing department phase")
    seen = set()
    for h in plan["handoffs"]:
        require(text(h["handoff_id"]) and h["handoff_id"] not in seen, "invalid handoff ID")
        seen.add(h["handoff_id"])
        require(h["from_task_id"] in task_map and h["to_task_id"] in task_map, "unknown handoff task")
        source, target = task_map[h["from_task_id"]], task_map[h["to_task_id"]]
        require(source["department_id"] != target["department_id"] and text(h["deliverable"]), "invalid cross-department handoff")
        ready, needed = h["ready_day"], h["needed_day"]
        require(type(ready) is int and type(needed) is int and ready < needed,
                "handoff must be ready at end of an earlier workday")
        require(ranges[source["phase_id"]][0] <= ready <= ranges[source["phase_id"]][1], "handoff ready outside source phase")
        require(ranges[target["phase_id"]][0] <= needed <= ranges[target["phase_id"]][1], "handoff needed outside target phase")
    for key in ["assumptions", "open_questions"]:
        require(isinstance(plan[key], list) and all(text(v) for v in plan[key]), "invalid " + key)


def validate_phase_personal(rows, department, plan):
    require(isinstance(rows, list), "personal plan must be an array")
    pairs = [(r["id"], r["phase_id"]) for r in rows]
    expected = {(i, p["phase_id"]) for i in department["member_ids"] for p in plan["phases"]}
    require(len(pairs) == len(set(pairs)) and set(pairs) == expected, "missing/duplicate employee-phase")
    tasks = {t["task_id"]: t for t in plan["department_tasks"] if t["department_id"] == department["id"]}
    covered = set()
    for row in rows:
        require(isinstance(row["detailed_goals"], list) and row["detailed_goals"]
                and all(text(g) for g in row["detailed_goals"]), "empty personal goals")
        refs = row["source_task_ids"]
        require(isinstance(refs, list) and refs and all(t in tasks and tasks[t]["phase_id"] == row["phase_id"] for t in refs),
                "wrong parent task or phase")
        covered.update(refs)
    require(covered == set(tasks), "unassigned department task")


def validate_phase_daily(rows, personal, plan, company, workday_range=None):
    require(isinstance(rows, list), "daily plan must be an array")
    start, end = phase_ranges(plan)[personal["phase_id"]]
    if workday_range is not None:
        require(start <= workday_range[0] <= workday_range[1] <= end, "batch outside phase")
        start, end = workday_range
    days = [r["workday"] for r in rows]
    require(all(type(d) is int for d in days) and len(days) == end - start + 1
            and set(days) == set(range(start, end + 1)), "daily plan must cover exactly its phase days")
    handoffs = {h["handoff_id"]: h for h in plan["handoffs"]}
    for row in rows:
        require(row["id"] == personal["id"] and row["phase_id"] == personal["phase_id"], "daily owner/phase mismatch")
        require(isinstance(row["activities"], list) and row["activities"], "missing activities")
        hours = 0
        for a in row["activities"]:
            require(text(a["description"]), "empty activity")
            require(type(a["hours"]) in (int, float) and math.isfinite(a["hours"]) and a["hours"] > 0, "invalid activity hours")
            hours += a["hours"]
            refs = a["source_task_ids"]
            require(isinstance(refs, list) and refs and all(t in personal["source_task_ids"] for t in refs), "daily task outside personal phase plan")
            needed = a["requires_handoff_ids"]
            require(isinstance(needed, list), "invalid dependencies")
            for h in needed:
                require(h in handoffs and handoffs[h]["to_task_id"] in refs, "unknown or unrelated handoff")
                require(row["workday"] >= handoffs[h]["needed_day"],
                        f"activity consumes handoff too early: {h} on workday {row['workday']}; earliest workday {handoffs[h]['needed_day']}")
            # A delivery can also be reused by its author or another department.
            # Such a data dependency is not a new, agreed department commitment.
            uses = a.get("uses_deliverable_ids", [])
            require(isinstance(uses, list), "invalid deliverable dependencies")
            for h in uses:
                require(h in handoffs, "unknown deliverable")
                require(row["workday"] > handoffs[h]["ready_day"],
                        f"activity uses deliverable before available: {h} on workday {row['workday']}; earliest workday {handoffs[h]['ready_day'] + 1}")
                if handoffs[h]["to_task_id"] in refs:
                    require(row["workday"] >= handoffs[h]["needed_day"],
                            f"activity consumes handoff too early: {h} on workday {row['workday']}; earliest workday {handoffs[h]['needed_day']}")
        require(hours <= company["hours_per_person_day"], "daily capacity exceeded")


PLAN_SCHEMA = '''{"phases":[{"phase_id":"P1","name":"Business phase name","duration_days":3,"goal":"phase outcome"}],
"department_tasks":[{"task_id":"P1-product","phase_id":"P1","department_id":"product","goal":"department outcome"}],
"handoffs":[{"handoff_id":"H1","from_task_id":"P1-product","to_task_id":"P2-engineering","deliverable":"agreed contract","ready_day":3,"needed_day":4}],
"assumptions":[],"open_questions":[]}'''


def participant_context(profile, prompt):
    return (f"\nEmployee ID: {profile['id']}.\nPersistent meeting context:\n" + prompt +
            "\nWhen assigned a subtask, give your own contribution within these shared constraints. "
            "Keep contributions concise, at most 500 words, unless consolidating the final JSON. "
            "Do not expand pilot scope beyond what the available people and days support.")


def company_context(company):
    return json.dumps({k: v for k, v in company.items() if k != "profiles"}, ensure_ascii=False) + (
        f"\nConfirmed employee count: {len(company['profiles'])}. "
        f"Confirmed total person-hours: {len(company['profiles']) * company['total_workdays'] * company['hours_per_person_day']}. "
        "Day numbers mean consecutive WORKDAYS, not calendar dates. All staff have the stated capacity. "
        "Planning occurs before day 1. Future deliverables are planned dependencies, not already-failed work. "
        "Do not claim work was executed or demand that future artifacts already exist. "
        "Do not invent reduced staff availability. Keep other assumptions explicitly tentative."
    )


def leadership_prompt(company):
    return ("Hold a leadership meeting. Obtain each department leader's planning view once, then consolidate. "
            "Choose business phases from the goal, total workdays, headcount and departmental skills. "
            "Decide the number of phases, their meaningful names and POSITIVE INTEGER duration_days yourself. "
            "Ordered phases are consecutive, non-overlapping, and their durations must sum exactly to total_workdays. "
            "No fixed weekly periods or Monday-Friday templates. Define one concise department task per department "
            "per phase, only at department level; personal allocation happens in the subsequent meetings. "
            "State cross-department handoffs using task IDs and global workday numbers. A deliverable is ready "
            "at END of ready_day and can first be required at START of a later needed_day. Both dates must "
            "fall inside their corresponding task's phase. Any infeasibility must be explicit. No work execution. "
            "Avoid excessive decomposition: one contribution per attending leader and a consolidation is enough. "
            "Final result must be a concise JSON object in this exact schema (example values are illustrative, "
            "not prescribed phases):\n" + PLAN_SCHEMA + "\nConfirmed company input:\n" + company_context(company))


def department_prompt(company, department, plan):
    return ("Hold a departmental planning meeting with the leader and every member. Give each attendee a voice, "
            "then consolidate. Use the agreed variable-duration phases unchanged. Allocate your department's tasks "
            "to each employee for EACH phase, including the leader; do not allocate by week. Preserve handoff dates. "
            "These are future execution plans, not plans merely to hold more planning meetings. A prerequisite "
            "scheduled for a future day is NOT blocked just because it does not exist before day 1. "
            "Only flag infeasibility supported by conflicting dates or capacity. No work execution. "
            "Keep output to 2-3 concrete goals per employee per phase. Final JSON array schema: "
            '[{"id":"employee ID","phase_id":"P1","detailed_goals":["specific future work"],"source_task_ids":["department task ID"]}].'
            "\nYour department: " + json.dumps(department, ensure_ascii=False) +
            "\nConfirmed company input:\n" + company_context(company) +
            "\nAgreed phase plan:\n" + json.dumps(plan, ensure_ascii=False) +
            "\nDerived inclusive workday ranges:\n" + json.dumps(phase_ranges(plan)))
