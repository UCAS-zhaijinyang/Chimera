"""Model and subprocess boundary for Phase 1 planning (loaded only for live work)."""
import getpass
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

from planning_io import dump, parse_json, read
from phase_planning import participant_context


def settings():
    import config
    keys = ("foundation_corp", "foundation_model", "llm_base_url", "llm_max_tokens", "llm_agent_max_tokens")
    result = {k: getattr(config, k) for k in keys}
    result["llm_agent_max_tokens"] = config.planning_agent_max_tokens
    return result


def credentials(hidden_prompt=False):
    import config
    if hidden_prompt:
        os.environ["CHIMERA_PLANNING_API_KEY"] = getpass.getpass("Model API key (hidden): ")
    override = os.environ.get("CHIMERA_PLANNING_API_KEY")
    if override:
        config.api_key = override
        if config.foundation_corp == "openai":
            os.environ["OPENAI_API_KEY"] = override


def create_meeting_model():
    import config
    if config.foundation_corp != "deepseek":
        from camel.models import ModelFactory
        from camel.types import ModelPlatformType
        from foundation_model import _qwen3_no_think_extra_body
        platforms = {"openai": ModelPlatformType.OPENAI, "google": ModelPlatformType.GEMINI,
                     "openai_compatible": ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
                     "xai": ModelPlatformType.OPENAI_COMPATIBLE_MODEL}
        if config.foundation_corp not in platforms:
            raise ValueError(f"Unsupported planning provider: {config.foundation_corp}")
        options = {"max_tokens": config.llm_agent_max_tokens, "tool_choice": "none"}
        extra = _qwen3_no_think_extra_body()
        if extra:
            options["extra_body"] = extra
        kwargs = {"model_platform": platforms[config.foundation_corp], "model_type": config.foundation_model,
                  "api_key": config.api_key or None, "model_config_dict": options, "timeout": 120}
        if config.foundation_corp == "openai_compatible":
            kwargs.update(url=config.llm_base_url, api_key=config.api_key or "EMPTY")
        elif config.foundation_corp == "xai":
            kwargs["url"] = "https://api.x.ai/v1"
        return ModelFactory.create(**kwargs)
    # Public CAMEL 0.2.45 treats max_tokens as its input-context capacity.
    # Separate these budgets without changing the original weekly meeting.
    from camel.models import DeepSeekModel
    from camel.types import ModelType

    class PlanningDeepSeekModel(DeepSeekModel):
        @property
        def token_limit(self):
            return 64000

    return PlanningDeepSeekModel(model_type=ModelType(config.foundation_model), api_key=config.api_key or None,
                                model_config_dict={"max_tokens": config.llm_agent_max_tokens, "tool_choice": "none"},
                                timeout=120)


def trace_api(out, limit=1000):
    """Capture OpenAI-compatible response evidence; never headers or credentials."""
    from openai.resources.chat.completions import Completions, AsyncCompletions
    guard, count = threading.Lock(), 0
    original, original_async = Completions.create, AsyncCompletions.create

    def start():
        nonlocal count
        with guard:
            if count >= limit:
                raise RuntimeError("Planning API-call limit reached")
            count += 1
            return count

    def record(number, kwargs, response, elapsed):
        entry = {"call": number, "seconds": round(elapsed, 3), "model": response.model,
                 "messages": kwargs.get("messages"), "usage": response.usage.model_dump() if response.usage else {},
                 "response": response.choices[0].message.model_dump(),
                 "finish_reason": response.choices[0].finish_reason}
        with guard, (Path(out) / "api_trace.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def sync(self, *args, **kwargs):
        number, started = start(), time.monotonic()
        response = original(self, *args, **kwargs)
        record(number, kwargs, response, time.monotonic() - started)
        return response

    async def asynchronous(self, *args, **kwargs):
        number, started = start(), time.monotonic()
        response = await original_async(self, *args, **kwargs)
        record(number, kwargs, response, time.monotonic() - started)
        return response

    Completions.create, AsyncCompletions.create = sync, asynchronous


def run_meeting_job(job_path):
    import config
    command = [sys.executable, str(Path(__file__).with_name("meeting_for_phase_goal_auto.py")), "--worker", str(job_path)]
    with (job_path.parent / "console.log").open("a", encoding="utf-8") as log:
        subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, env=dict(os.environ),
                       timeout=getattr(config, "planning_meeting_timeout", 900), check=True)


def meeting_worker(job_path):
    import config
    job_path = Path(job_path)
    job, folder = read(job_path), job_path.parent
    for key, value in job["runtime"].items():
        if key not in settings():
            raise ValueError(f"Unexpected runtime option: {key}")
        setattr(config, key, value)
    credentials()
    config.company_type = job["company"]["company_type"]
    config.goal = job["company"]["goal"]
    config.employee_number = len(job["company"]["profiles"])
    config.meeting_log_dir = str(folder)
    trace_api(folder, limit=getattr(config, "planning_max_api_calls", 1000))
    from camel.agents import ChatAgent
    from camel.societies.workforce import Workforce
    from camel.tasks.task import Task
    import meeting_for_weekly_goal_auto as original_meeting
    original_meeting.create_meeting_camel_model = create_meeting_model
    feedback = ""
    offset = len(list(folder.glob("meeting_result.attempt*.log")))
    for attempt in range(getattr(config, "planning_meeting_rounds", 3)):
        prompt = job["prompt"] + feedback
        kwargs = {"model": create_meeting_model()}
        workforce = Workforce("Business phase planning meeting", coordinator_agent_kwargs=kwargs,
                              task_agent_kwargs=kwargs, new_worker_agent_kwargs=kwargs)
        attendees = []
        for member_id in job["meeting"]["member_ids"]:
            profile, original = original_meeting.load_member_profile(str(folder / "members" / (member_id + ".jsonc")), [])
            message = original.system_message.create_new_instance(
                original.system_message.content + participant_context(profile, prompt))
            agent = ChatAgent(message, model=create_meeting_model())
            workforce.add_single_agent_worker(f"{member_id}: {profile['role']}-{profile['name']}", worker=agent)
            attendees.append({k: profile[k] for k in ("id", "name", "role")})
        task = Task(content=prompt + "\nActual meeting attendees (not the entire company):\n" + json.dumps(attendees), id=str(attempt))
        result = original_meeting.process_task_logging(workforce, task, str(folder / f"round_{offset + attempt + 1}"))
        raw = result.result or ""
        (folder / f"meeting_result.attempt{offset + attempt + 1}.log").write_text(raw, encoding="utf-8")
        try:
            value = parse_json(raw)
            # Validate the artifact at the meeting boundary so an LLM proposal
            # that is valid JSON but violates the planning contract is retried
            # with actionable feedback instead of being persisted.
            if job["meeting"]["id"] == "leadership":
                from phase_planning import validate_phase_plan
                validate_phase_plan(value, job["company"])
            else:
                from phase_planning import validate_phase_personal
                department = next(d for d in job["company"]["departments"]
                                  if d["id"] == job["meeting"]["department_id"])
                validate_phase_personal(value, department, job["meeting_context"])
            (folder / "meeting_result.log").write_text(raw, encoding="utf-8")
            return
        except (ValueError, KeyError, TypeError) as exc:
            dump(folder / f"validation_error.attempt{offset + attempt + 1}.json", {"error": str(exc)})
            feedback = ("\nRECONVENE: the proposal failed validation: " + str(exc) +
                        "\nAll attendees must agree a revision within the original resource constraints. "
                        "End-of-day delivery cannot support start-of-the-same-day consumption. "
                        "Return the complete JSON proposal. Previous proposal:\n" + raw)
    raise ValueError("Meeting still invalid; proposals retained for inspection")
