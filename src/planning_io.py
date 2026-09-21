"""Persistent contracts between Phase 1 planning programs; no model imports."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

import json5

from phase_planning import (build_phase_meetings, require, validate_phase_personal,
                            validate_phase_plan)

SCHEMA_VERSION = 1


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, value):
    """Publish one complete JSON artifact atomically, including across workers."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".planning-", delete=False) as stream:
            temporary = stream.name
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def parse_json(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(raw)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def prepare_output(path, manifest, resume=False):
    path = Path(path)
    if path.exists():
        require(resume, f"Output exists: {path}; use --resume or a new output directory")
        require((path / "manifest.json").is_file(), "Output has no manifest; use a new directory")
        require(read(path / "manifest.json") == manifest, "Cannot resume: input or settings changed")
    else:
        path.mkdir(parents=True)
        dump(path / "manifest.json", manifest)


def _role_groups(node, path=()):
    groups = []
    if isinstance(node, dict):
        if isinstance(node.get("roles"), list) and node["roles"]:
            label = "__".join(path) or "company"
            identifier = label if re.fullmatch(r"[A-Za-z0-9_-]+", label) else "dept_" + fingerprint(label)[:12]
            members, leaders = [], []
            for role in node["roles"]:
                require(type(role.get("count")) is int and role["count"] >= 0, "Invalid role count")
                ids = [f"{role['abbr']}-{i + 1}" for i in range(role["count"])]
                members.extend(ids)
                if role.get("is_leader") is True:
                    leaders.extend(ids)
            if members:
                group = {"id": identifier, "member_ids": members}
                if node.get("leader_id"):
                    group["leader_id"] = node["leader_id"]
                elif leaders:
                    group["_role_leaders"] = leaders
                if label != identifier:
                    group["name"] = label
                groups.append(group)
        for key, child in node.items():
            if key != "roles" and isinstance(child, (dict, list)):
                groups.extend(_role_groups(child, path + (key,)))
    elif isinstance(node, list):
        for i, child in enumerate(node):
            groups.extend(_role_groups(child, path + (str(i),)))
    return groups


def load_company(profile_dir, organization_path, *, goal, company_type, total_workdays,
                 hours_per_person_day, leaders=None):
    """Read existing generated profiles and explicit organization relationships."""
    folder = Path(profile_dir)
    paths = sorted(p for p in folder.iterdir() if p.suffix in (".json", ".jsonc"))
    profiles = [json5.loads(p.read_text(encoding="utf-8")) for p in paths]
    require(profiles, f"No employee profiles in {folder}")
    members = {p["id"]: p for p in profiles}
    require(len(members) == len(profiles), "Duplicate profile IDs")
    organization = json5.loads(Path(organization_path).read_text(encoding="utf-8")) if organization_path else {}
    leaders = leaders or {}
    if isinstance(organization.get("departments"), list):
        groups = [dict(d) for d in organization["departments"]]
    elif all(p.get("department_id") for p in profiles):
        grouped = {}
        for p in profiles:
            grouped.setdefault(p["department_id"], []).append(p["id"])
        groups = [{"id": d, "member_ids": ids} for d, ids in grouped.items()]
    else:
        groups = _role_groups(organization)
    require(groups, "No departments: provide department_id in profiles or company roles hierarchy")
    require(set(leaders) <= {d["id"] for d in groups}, "Unknown department in planning_department_leaders")
    for group in groups:
        ids = group["member_ids"]
        require(set(ids) <= members.keys(), f"Missing profile for department {group['id']}: {set(ids) - members.keys()}")
        leader = leaders.get(group["id"], group.get("leader_id"))
        role_leaders = group.pop("_role_leaders", [])
        if not leader:
            marked = sorted(set(role_leaders) | {i for i in ids if members[i].get("is_leader") is True})
            require(len(marked) <= 1, f"Ambiguous leader flags for {group['id']}: {marked}; set planning_department_leaders")
            if len(marked) == 1:
                leader = marked[0]
            elif len(ids) == 1:
                leader = ids[0]
            elif all("reports_to" in members[i] for i in ids):
                roots = [i for i in ids if members[i]["reports_to"] not in ids]
                if len(roots) == 1:
                    leader = roots[0]
                    for member_id in ids:
                        visited, current = set(), member_id
                        while current != leader:
                            require(current in ids and current not in visited, "Invalid reporting hierarchy")
                            visited.add(current)
                            current = members[current]["reports_to"]
        require(leader in ids, f"Ambiguous/missing leader for {group['id']}; set planning_department_leaders[{group['id']!r}] to one of {ids}")
        group["leader_id"] = leader
    result = {"company_type": company_type, "goal": goal, "total_workdays": total_workdays,
              "hours_per_person_day": hours_per_person_day, "departments": groups, "profiles": profiles}
    build_phase_meetings(result)
    return result


def validate_bundle(bundle):
    require(bundle.get("schema_version") == SCHEMA_VERSION, "Unsupported phase plan schema_version")
    company = bundle["company"]
    build_phase_meetings(company)
    plan, personal = bundle["phase_plan"], bundle["personal_plans"]
    validate_phase_plan(plan, company)
    require(len(personal) == len(company["profiles"]) * len(plan["phases"]), "Incomplete employee-phase coverage")
    for department in company["departments"]:
        validate_phase_personal([r for r in personal if r["id"] in department["member_ids"]], department, plan)
    return bundle


def load_bundle(path):
    try:
        return validate_bundle(read(path))
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError(f"Invalid/incomplete phase plan bundle: {exc}") from exc
