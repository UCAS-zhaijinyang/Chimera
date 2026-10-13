# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
import os
import json
import copy
import hashlib
import re
import tempfile
import shutil
import config
from foundation_model import run_llm
from daily_attack_schedule import (
    generate_attack_schedule,
    update_daily_schedule_with_attack,
)
import argparse


def _strip_json_fence(output):
    text = str(output).strip()
    if "```" in text:
        text = text.replace("```json", "").replace("```JSON", "")
        text = text.replace("```", "").strip()
    return text


def validate_campaign_plan(plan, normal_schedules, attack_info):
    """Validate an LLM campaign plan against frozen normal schedule keys."""
    if not isinstance(normal_schedules, dict) or not normal_schedules:
        raise ValueError("normal_schedules must be a nonempty mapping")
    if not isinstance(plan, dict) or not isinstance(plan.get("days"), list):
        raise ValueError("campaign plan must contain a days array")
    if not plan["days"]:
        raise ValueError("campaign plan must select at least one day")

    expected = [item.get("step") for item in attack_info.get("how", [])]
    if not expected or any(type(step) is not int for step in expected):
        raise ValueError("attack info must contain integer how steps")
    if len(expected) != len(set(expected)):
        raise ValueError("attack info contains duplicate steps")

    normalized_days = []
    selected = set()
    covered = []
    for item in plan["days"]:
        if not isinstance(item, dict):
            raise ValueError("each campaign day must be an object")
        date_key = item.get("date", item.get("schedule_key"))
        if not isinstance(date_key, str) or date_key not in normal_schedules:
            raise ValueError(f"unknown campaign schedule date: {date_key}")
        if date_key in selected:
            raise ValueError(f"campaign date selected more than once: {date_key}")
        steps = item.get("attack_steps")
        if (
            not isinstance(steps, list)
            or not steps
            or any(type(step) is not int for step in steps)
        ):
            raise ValueError(f"invalid attack_steps for {date_key}")
        if any(step not in expected for step in steps):
            raise ValueError(f"unknown attack step in {date_key}")
        selected.add(date_key)
        covered.extend(steps)
        normalized_days.append(
            {
                "date": date_key,
                "attack_steps": list(steps),
                "purpose": str(item.get("purpose", "")).strip(),
            }
        )

    if covered != expected:
        raise ValueError("campaign days must cover every specified step in order")
    normalized = dict(plan)
    normalized["attack_id"] = plan.get("attack_id", attack_info.get("attack_id"))
    normalized["days"] = normalized_days
    return normalized


def plan_attack_campaign_with_gpt(
    normal_schedules, member_profile, attack_info, id_role_map
):
    """Ask the LLM to place all attack steps over one or more normal days."""
    attack_summary = {
        "attack_id": attack_info.get("attack_id"),
        "what": attack_info.get("what"),
        "type": attack_info.get("type"),
        "how": attack_info.get("how", []),
        "when": attack_info.get("when", {}),
        "who": attack_info.get("who", {}),
    }
    system_prompt = f"""You are {member_profile.get('name', 'the employee')}, {member_profile.get('role', 'employee')} at a company.
You are planning one insider attack campaign over a complete frozen normal schedule.
Attack details: {json.dumps(attack_summary, ensure_ascii=False)}
Choose one or more existing schedule keys whose normal activities can conceal the attack.
Assign every attack step exactly once, in order across the selected days. Do not invent dates,
do not rewrite unselected days, and do not force a fixed number of days.
Return ONLY JSON with this shape:
{{"days":[{{"date":"existing schedule key","attack_steps":[1],"purpose":"brief reason"}}]}}"""
    user_prompt = (
        "Employee/team context: "
        + json.dumps(id_role_map, ensure_ascii=False)
        + "\nComplete frozen normal schedule:\n"
        + json.dumps(normal_schedules, ensure_ascii=False)
    )
    last_error = None
    for attempt in range(config.max_attempt):
        try:
            raw_output = run_llm(system_prompt, user_prompt, temperature=0.7)
            parsed = json.loads(_strip_json_fence(raw_output))
            parsed["raw_llm_output"] = str(raw_output)
            return validate_campaign_plan(parsed, normal_schedules, attack_info)
        except Exception as exc:
            last_error = exc
            print(f"[WARN] Invalid multi-day campaign plan (attempt {attempt + 1}): {exc}")
            if attempt == config.max_attempt - 1:
                raise ValueError("campaign planning exhausted retries") from exc
    raise AssertionError(last_error)


def _subset_attack_info(attack_info, steps):
    subset = copy.deepcopy(attack_info)
    by_step = {item["step"]: item for item in attack_info.get("how", [])}
    subset["how"] = [by_step[step] for step in steps]
    return subset


def _schedule_file_name(member_id, schedule_key):
    safe_key = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(schedule_key))
    return f"{member_id}_{safe_key}_attack.json"


def _json_hash(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def apply_campaign_plan(
    normal_schedules,
    campaign_plan,
    member_id,
    attack_id,
    id_role_map,
    *,
    output_dir=None,
    member_profile=None,
    attack_info=None,
):
    """Apply a validated campaign atomically and return its audit manifest."""
    if attack_info is None:
        with open(os.path.join(config.attack_dir, f"{attack_id}.json"), "r") as f:
            attack_info = json.load(f)
    campaign_plan = validate_campaign_plan(campaign_plan, normal_schedules, attack_info)
    if member_profile is None:
        with open(os.path.join(config.profile_output_dir, f"{member_id}.jsonc"), "r") as f:
            member_profile = json.load(f)

    selected = {item["date"]: item for item in campaign_plan["days"]}
    modified = {}
    for schedule_key, normal_schedule in normal_schedules.items():
        frozen = copy.deepcopy(normal_schedule)
        if schedule_key in selected:
            day_info = selected[schedule_key]
            day_attack_info = _subset_attack_info(
                attack_info, day_info["attack_steps"]
            )
            edited = generate_attack_schedule(
                copy.deepcopy(frozen), member_profile, day_attack_info, id_role_map
            )
            modified[schedule_key] = copy.deepcopy(edited)
        else:
            modified[schedule_key] = frozen

    destination = output_dir or config.attack_schedule_dir
    os.makedirs(destination, exist_ok=True)
    day_manifest = {}
    for schedule_key, normal_schedule in normal_schedules.items():
        day_manifest[schedule_key] = {
            "selected": schedule_key in selected,
            "normal_schedule": copy.deepcopy(normal_schedule),
            "modified_schedule": copy.deepcopy(modified[schedule_key]),
            "normal_sha256": _json_hash(normal_schedule),
            "modified_sha256": _json_hash(modified[schedule_key]),
        }
        if schedule_key in selected:
            day_manifest[schedule_key]["attack_steps"] = selected[schedule_key]["attack_steps"]

    manifest = {
        "schema_version": "chimera-attack-campaign/1",
        "member_id": member_id,
        "attack_id": attack_id,
        "selected_dates": list(selected),
        "campaign_plan": copy.deepcopy(campaign_plan),
        "days": day_manifest,
    }
    manifest_path = os.path.join(destination, f"{member_id}_{attack_id}_campaign.json")

    # Stage every output in a private directory.  A failed write cannot leave
    # a partially materialized campaign visible to the daily executor.
    staging_dir = tempfile.mkdtemp(prefix=".campaign-", dir=destination)
    try:
        for schedule_key in selected:
            staged_name = _schedule_file_name(member_id, schedule_key)
            staged_path = os.path.join(staging_dir, staged_name)
            with open(staged_path, "w", encoding="utf-8") as f:
                json.dump(modified[schedule_key], f, indent=4, ensure_ascii=False)
            day_manifest[schedule_key]["output_path"] = os.path.join(destination, staged_name)
        staged_manifest = os.path.join(staging_dir, os.path.basename(manifest_path))
        with open(staged_manifest, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        for filename in os.listdir(staging_dir):
            os.replace(
                os.path.join(staging_dir, filename),
                os.path.join(destination, filename),
            )
    finally:
        shutil.rmtree(staging_dir, ignore_errors=True)
    manifest["manifest_path"] = manifest_path
    return manifest


def load_member_normal_schedules(member_id, schedule_dir=None):
    """Load every existing normal day for a member as stable schedule keys."""
    root = schedule_dir or config.init_schedule_dir
    schedules = {}
    week_names = sorted(os.listdir(root)) if os.path.isdir(root) else []
    for week_name in week_names:
        week_dir = os.path.join(root, week_name)
        if not os.path.isdir(week_dir):
            continue
        match = re.fullmatch(r"week_(\d+)", week_name)
        if not match:
            continue
        week = match.group(1)
        prefix = f"{member_id}_week_{week}_"
        for filename in sorted(os.listdir(week_dir)):
            if not filename.startswith(prefix) or not filename.endswith(".json"):
                continue
            date = filename[len(prefix):-5]
            with open(os.path.join(week_dir, filename), "r", encoding="utf-8") as f:
                schedules[f"week_{week}_{date}"] = json.load(f)
    if not schedules:
        raise FileNotFoundError(f"no normal schedules found for {member_id}")
    return schedules


def inject_attack_campaigns(attacker_attack_map, id_role_map, *, output_dir=None):
    """Plan and materialize multi-day campaigns for the new framework."""
    manifests = {}
    for member_id, attack_id in attacker_attack_map.items():
        normal_schedules = load_member_normal_schedules(member_id)
        with open(os.path.join(config.profile_output_dir, f"{member_id}.jsonc"), "r") as f:
            member_profile = json.load(f)
        with open(os.path.join(config.attack_dir, f"{attack_id}.json"), "r") as f:
            attack_info = json.load(f)
        campaign_plan = plan_attack_campaign_with_gpt(
            normal_schedules, member_profile, attack_info, id_role_map
        )
        manifests[member_id] = apply_campaign_plan(
            normal_schedules,
            campaign_plan,
            member_id,
            attack_id,
            id_role_map,
            output_dir=output_dir,
            member_profile=member_profile,
            attack_info=attack_info,
        )
    return manifests


def write_campaign_bundle(manifests, output_path):
    """Persist all attacker campaign manifests for later per-day runs."""
    payload = {
        "schema_version": "chimera-attack-campaign-bundle/1",
        "campaigns": manifests,
    }
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return output_path


def load_campaign_bundle(bundle_path):
    with open(bundle_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    campaigns = payload.get("campaigns")
    if not isinstance(campaigns, dict) or not campaigns:
        raise ValueError("campaign bundle must contain a nonempty campaigns object")
    return campaigns


def restore_campaign_files(manifests, output_dir=None):
    """Restore selected-day files from a saved bundle before daily execution."""
    destination = output_dir or config.attack_schedule_dir
    os.makedirs(destination, exist_ok=True)
    restored = []
    for member_id, manifest in manifests.items():
        for schedule_key in manifest.get("selected_dates", []):
            day = manifest.get("days", {}).get(schedule_key)
            if not day or "modified_schedule" not in day:
                raise ValueError(f"campaign bundle is missing {member_id}/{schedule_key}")
            filename = _schedule_file_name(member_id, schedule_key)
            path = os.path.join(destination, filename)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(day["modified_schedule"], f, indent=4, ensure_ascii=False)
            restored.append(path)
    return restored


def select_attack_date(attacker, attack_id, id_role_map):
    # scenarios = ["tech_company", "finance_corporation", "medical_institution"]
    # attacker_ids = ["cdev-1", "qres-1", "his-1"]
    weeks = [1, 2, 3, 4]
    dates = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    attack_info_path = os.path.join(config.attack_dir, f"{attack_id}.json")

    with open(attack_info_path, "r") as f:
        attack_info = json.load(f)

    ### pick the right day to attack
    # read all existing schedule
    schedule_path = config.init_schedule_dir

    total_schedule = {}

    for week in weeks:
        for date in dates:
            schedule_file = os.path.join(
                schedule_path, f"week_{week}", f"{attacker}_week_{week}_{date}.json"
            )
            if os.path.exists(schedule_file):
                with open(schedule_file, "r") as f:
                    schedule = json.load(f)
                key_name = f"week_{week}_{date}"
                total_schedule[key_name] = schedule

    system_prompt = f"""You are an attacker in the company. The details of your attack are as follows: {attack_info}.
                        I will provide you with the overall schedule of each day, and you should reply with the most suitable day you select to attack to conceal your attacks and take the most of the attack effect.
                        **You should only reply with the data in the format of "week_{{week number}}_{{date}}" and do not reply with anything else**. The date should be in the format of "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", or "Sunday". The week number should be an integer. For example, if you want to attack on the first Monday, you should reply with "week_1_Monday". If you want to attack on the third Friday, you should reply with "week_3_Friday".
                    """
    user_prompt = f"The overall schedule of each day is as follows: {total_schedule}"

    for i in range(config.max_attempt):
        try:
            llm_output = run_llm(system_prompt, user_prompt, temperature=0.7)
            llm_output = llm_output.strip()
            if llm_output.startswith("week_") and len(llm_output.split("_")) == 3:
                attack_week = int(llm_output.split("_")[1])
                attack_date = llm_output.split("_")[2]
                break
        except Exception as e:
            print(f"Error: {e}")
            if i == config.max_attempt - 1:
                raise

    ### update the schedule
    print(
        f"Attack {attack_id} scheduled on week {attack_week} - {attack_date} by {attacker}"
    )
    update_daily_schedule_with_attack(
        attack_week, attack_date, attacker, attack_id, id_role_map
    )
    return attack_week, attack_date


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Attack selection and scheduling")
    parser.add_argument(
        "--attacker", type=str, required=True, help="Attacker id, e.g., cdev-1"
    )
    parser.add_argument(
        "--attid", type=str, required=True, help="Attack id, e.g., gen_attack_1"
    )
    args = parser.parse_args()

    attacker = args.attacker
    attack_id = args.attid

    ########################
    # Get the total employee info
    id_role_map = {}
    id_list = []
    profile_list = []

    member_dir = config.profile_output_dir
    for file in os.listdir(member_dir):
        if file.endswith(".jsonc"):
            member_profile_path = os.path.join(member_dir, file)
            with open(member_profile_path, "r") as f:
                member_profile = json.load(f)
            id_role_map[member_profile["id"]] = member_profile[
                "role"
            ]  # add id-role map
            id_list.append(member_profile["id"])
            profile_list.append(member_profile)  # add profile

    ########################
    select_attack_date(attacker, attack_id, id_role_map)
