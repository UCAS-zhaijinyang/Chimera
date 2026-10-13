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
from dotenv import load_dotenv
import os

import json
from datetime import datetime

from foundation_model import run_llm

import config

env_path = config.env_path
load_dotenv()


def attack_daily_schedule_with_gpt(
    initial_schedule, member_profile, attack_info, id_role_map
):
    attack_summary = {
        "attack_id": attack_info.get("attack_id"),
        "what": attack_info.get("what"),
        "type": attack_info.get("type"),
        "how": attack_info.get("how", []),
        "when": attack_info.get("when", {}),
        "who": attack_info.get("who", {}),
    }
    system_prompt = f"""You are {member_profile['name']}, {member_profile['role']} at a {config.company_type}.
You are also the insider attacker. Goal: {attack_summary['what']}.
Work hours: {config.work_start}-{config.work_end}. Team: {id_role_map}.
Update today's schedule JSON to blend normal work with attack steps.
Return ONLY a JSON array of objects with keys "Time" (HH:MM:SS), "Activity", and optional "Attack": true.
Every attack slot must include "AttackSteps": [step numbers covered by that activity].
Cover ALL how steps in order, exactly once; combine steps only when the activity explicitly includes them.
Use @id for email contacts. Preserve normal work; allocate as many slots as needed.
Respect the attack time_window: after-hours steps must be outside work hours."""
    user_prompt = f"""Previous schedule: {initial_schedule}
Attack details: {attack_summary}"""

    llm_output = run_llm(system_prompt, user_prompt, temperature=0.7)
    return llm_output


def validate_attack_schedule(schedule, attack_info):
    """Reject lost steps and malformed schedules before committing injection."""
    if not isinstance(schedule, list) or not schedule:
        raise ValueError('attack schedule must be a nonempty array')
    expected = [row['step'] for row in attack_info.get('how', [])]
    covered, times = [], []
    window = attack_info.get('when', {}).get('time_window')
    start = datetime.strptime(config.work_start, '%H:%M').time()
    end = datetime.strptime(config.work_end, '%H:%M').time()
    for row in schedule:
        if not isinstance(row, dict) or not isinstance(row.get('Activity'), str) or not row['Activity'].strip():
            raise ValueError('invalid attack activity')
        timestamp = datetime.strptime(row['Time'], '%H:%M:%S').time()
        times.append(timestamp)
        if 'Attack' in row and type(row['Attack']) is not bool:
            raise ValueError('Attack must be a boolean')
        if row.get('Attack'):
            steps = row.get('AttackSteps')
            if not isinstance(steps, list) or not steps or any(type(n) is not int for n in steps):
                raise ValueError('attack activity must identify covered steps')
            covered.extend(steps)
            if window == 'after hours' and start <= timestamp < end:
                raise ValueError('after-hours attack scheduled during work')
            if window == 'work hours' and not start <= timestamp < end:
                raise ValueError('work-hours attack scheduled outside work')
    if times != sorted(times) or len(times) != len(set(times)):
        raise ValueError('schedule times must be ordered and unique')
    if covered != expected:
        raise ValueError('attack schedule must cover every specified step in order')
    by_step = {step['step']: step for step in attack_info.get('how', [])}
    for row in schedule:
        if row.get('Attack'):
            requirements = [by_step[n] for n in row['AttackSteps']]
            # The executor consumes Activity. Bind canonical text deterministically
            # rather than relying on an LLM's step-number claim.
            base = row['Activity'].split('\nCanonical attack requirements:\n', 1)[0]
            row['AttackRequirements'] = requirements
            row['Activity'] = base + '\nCanonical attack requirements:\n' + json.dumps(requirements, ensure_ascii=False)
    return schedule


def update_daily_schedule_with_attack(week, date, member_id, attack_id, id_role_map):
    # Load the member profile
    member_profile = json.load(open(f"{config.profile_output_dir}/{member_id}.jsonc"))
    # Load initial schedule
    # if the schedule does not exist, use an empty schedule as default
    if os.path.exists(
        f"{config.init_schedule_dir}/week_{week}/{member_id}_week_{week}_{date}.json"
    ):
        # if not exist then choose the first schedule in the week as default
        with open(
            f"{config.init_schedule_dir}/week_{week}/{member_id}_week_{week}_{date}.json",
            "r",
        ) as f:
            initial_schedule = json.load(f)
    else:
        with open(
            f"{config.init_schedule_dir}/week_{week}/{member_id}_week_{week}_Monday.json",
            "r",
        ) as f:
            initial_schedule = json.load(f)
    # Load the attack info
    with open(f"{config.attack_dir}/{attack_id}.json", "r") as f:
        attack_info = json.load(f)

    # Generate new schedule
    for attempt in range(config.max_attempt):
        output_schedule = attack_daily_schedule_with_gpt(
            initial_schedule, member_profile, attack_info, id_role_map
        )
        # # Parse the response to extract the updated schedule
        if "```json" in output_schedule:
            output_schedule = (
                output_schedule.replace("```json", "").replace("```", "").strip()
            )

        try:
            new_schedule = validate_attack_schedule(json.loads(output_schedule), attack_info)
            break
        except Exception as e:
            print("[WARN] Error parsing JSON:", e, "Retrying...")
            if attempt == config.max_attempt - 1:
                print("[Error] Max attempts reached. Do not update the schedule.")
                raise ValueError('attack schedule generation exhausted retries; previous schedule preserved') from e

    # print(f"### New Schedule ### : {new_schedule}")
    if not os.path.exists(config.attack_schedule_dir):
        os.makedirs(config.attack_schedule_dir, exist_ok=True)
    # Save the new schedule
    with open(
        f"{config.attack_schedule_dir}/{member_id}_week_{week}_{date}_attack.json", "w"
    ) as f:
        json.dump(new_schedule, f, indent=4)


if __name__ == "__main__":
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
    week = 1
    date = "Friday"
    member_id = "cdev-1"
    attack_id = "gen_attack_1"

    update_daily_schedule_with_attack(week, date, member_id, attack_id, id_role_map)
