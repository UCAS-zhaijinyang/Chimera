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
# system config
import os

from dotenv import load_dotenv

base_dir = os.environ.get("CHIMERA_BASE_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = f"{base_dir}/.env"
load_dotenv(env_path)


def normalize_openai_compatible_base_url(value):
    """Accept either an OpenAI base URL or a full chat-completions endpoint."""
    url = (value or "").strip().rstrip("/")
    for suffix in ("/chat/completions", "/completions"):
        if url.endswith(suffix):
            url = url[: -len(suffix)]
            break
    return url.rstrip("/")

# scenario name
scenario_name = os.environ.get("CHIMERA_SCENARIO", "chimera_scenario_100d")

# company_id = "tech_company" ###### 2 #######
# company_id = "finance_corporation"
company_id = os.environ.get("CHIMERA_COMPANY_ID", "medical_institution")

# company_type = "Game Company"
# company_type = "Finance Corporation (Quantitative Hedge Fund)" #
company_type = os.environ.get(
    "CHIMERA_COMPANY_TYPE", "Medical Institution (Small Community Hospital)"
)  ###### 3 #######

# profile output directory
profile_output_dir = f"{base_dir}/{scenario_name}/generated_members"
# attack directory
attack_dir = os.environ.get("CHIMERA_ATTACK_DIR", f"{base_dir}/attacks")
# attack log directory
attack_schedule_dir = f"{base_dir}/{scenario_name}/attack_schedule"

company_config_path = f"{base_dir}/{scenario_name}/team/{company_id}.json"

# meeting log directory
meeting_log_dir = f"{base_dir}/{scenario_name}/meeting_logs"
# Phase 1 meeting and plan-generation artifacts.
leadership_meeting_dir = f"{meeting_log_dir}/leadership_meetings"
department_phase_plan_path = f"{meeting_log_dir}/department_phase_plans.json"
department_meeting_dir = f"{meeting_log_dir}/department_meetings"
# Complete employee-phase handoff to the independent daily-plan program.
phase_plan_path = f"{meeting_log_dir}/phase_plans.json"
# initial schedule directory
init_schedule_dir = f"{base_dir}/{scenario_name}/init_schedule"
# execution log directory
execution_log_dir = f"{base_dir}/{scenario_name}/execution_logs"
# attack log directory
attack_log_dir = f"{base_dir}/{scenario_name}/attack_logs"

# goal of the company
# goal = "The goal of your company is to construct a Third-person shooter game from the beginning." ####### 4 #######
# goal = "The goal of your company is to design and register a market-neutral statistical arbitrage fund targeting UHNWIs (Ultra-High-Net-Worth Individuals) under SEC regulations from the beginning."
goal = os.environ.get(
    "CHIMERA_GOAL",
    "The goal of your institution (small community hospital) is to complete electronic health record collection and seasonal influenza trend analysis from the beginning.",
)

period = 20  # Legacy weekly meeting only; the phase pipeline never reads this.
total_workdays = int(os.environ.get("CHIMERA_TOTAL_WORKDAYS", "100"))
employee_number = int(os.environ.get("CHIMERA_EMPLOYEE_NUMBER", "90"))

# date for starters
base_date = "2026-08-28"

# Simulated workday hours used when generating / updating schedules.
work_start = "10:00"
work_end = "18:00"
planning_hours_per_day = 8
# Explicit overrides keyed by department ID / nested role-tree path joined with __.
# Needed only when leader_id, is_leader or a unique reports_to root is unavailable.
planning_department_leaders = {}
planning_workers = int(os.environ.get("CHIMERA_PLANNING_WORKERS", "3"))
planning_daily_batch_days = int(os.environ.get("CHIMERA_PLANNING_BATCH_DAYS", "5"))
planning_meeting_rounds = int(os.environ.get("CHIMERA_PLANNING_MEETING_ROUNDS", "3"))
planning_meeting_timeout = int(os.environ.get("CHIMERA_PLANNING_MEETING_TIMEOUT", "900"))
planning_max_api_calls = int(os.environ.get("CHIMERA_PLANNING_MAX_API_CALLS", "1000"))
planning_agent_max_tokens = int(os.environ.get("CHIMERA_PLANNING_AGENT_MAX_TOKENS", "4096"))
# Hard stop for the Phase-2 day simulation loop (HH:MM:SS).
sim_day_end = "19:00:00"

# maximum number of attempts for query LLM for structured output
max_attempt = 5
# maximum query loop
round_limit = 5
# Cap internal tool-calling iterations inside a single ChatAgent.step/astep.
# Prevents unbounded while-True tool loops when context truncation forces retries.
max_tool_iterations = 20
# Opt-in filesystem workflow runner.  The legacy OWL/CAMEL path remains the
# default so existing Phase 2 experiments are reproducible.
workflow_execution_enabled = os.environ.get("CHIMERA_WORKFLOW_EXECUTION", "0").lower() in {"1", "true", "yes"}
workflow_api_timeout = int(os.environ.get("CHIMERA_WORKFLOW_API_TIMEOUT", "90"))
workflow_max_steps = int(os.environ.get("CHIMERA_WORKFLOW_MAX_STEPS", "24"))
# Wall-clock timeout for a single Phase-2 OWL task subprocess (seconds).
# Timed-out / unfinished workers are killed by the process registry.
task_process_timeout = 600

# loaf parameters
loaf_rate = 0.3
loaf_interval = 40

# time simulation
sim_seconds = 15
interval_seconds = 5

# Set to True to disable all external network requests (browser, search engines).
# Recommended for isolated/containerized deployments as described in the paper.
offline_mode = True

### Foundation Model
# Local OpenAI-compatible endpoint from .env (LLM_MODEL_ID + LLM_BASE_URL)
# takes precedence over the cloud provider below.
llm_model_id = os.environ.get("LLM_MODEL_ID", "").strip()
llm_base_url = normalize_openai_compatible_base_url(
    os.environ.get("LLM_BASE_URL", "")
)
llm_api_key = os.environ.get("LLM_API_KEY", "").strip() or "EMPTY"

# Explicit GLM provider alias.  The endpoint may be supplied as either the
# full /v1/chat/completions URL or its OpenAI-compatible /v1 base URL.
glm_endpoint = (
    os.environ.get("GLM_ENDPOINT", "").strip()
    or os.environ.get("GLM_BASE_URL", "").strip()
)
glm_model_id = os.environ.get("GLM_MODEL_ID", "").strip()
glm_api_key = os.environ.get("GLM_API_KEY", "").strip()
if glm_endpoint:
    llm_model_id = glm_model_id or "GLM-5.3"
    llm_base_url = normalize_openai_compatible_base_url(glm_endpoint)
    llm_api_key = glm_api_key or llm_api_key
# Local vLLM endpoint (current server: max_model_len=16384, tool calling enabled).
llm_max_tokens = int(os.environ.get("LLM_MAX_TOKENS", "4096"))
llm_agent_max_tokens = int(os.environ.get("LLM_AGENT_MAX_TOKENS", "2048"))
local_llm_disable_tools = False

### openai
# foundation_corp = "openai"
# foundation_model = "gpt-4o-mini"

### google
# foundation_corp = "google"
# foundation_model = "gemini-2.0-flash"
# api_key = 'XXX'

### deepseek
foundation_corp = "deepseek"
foundation_model = "deepseek-chat"
api_key = os.environ.get("DEEPSEEK_API_KEY", "")

# ### grok
# foundation_corp = "xai"
# foundation_model = "grok-3-mini"
# api_key = "XXX"

if llm_model_id and llm_base_url:
    foundation_corp = "openai_compatible"
    foundation_model = llm_model_id
    api_key = llm_api_key
