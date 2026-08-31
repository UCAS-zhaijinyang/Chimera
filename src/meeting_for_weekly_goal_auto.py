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
from camel.agents.chat_agent import ChatAgent
from camel.messages.base import BaseMessage
from camel.societies.workforce import Workforce
from camel.tasks.task import Task
from camel.toolkits import (
    FunctionTool,
    SearchToolkit,
)
import logging
import os
from camel.logger import set_log_level

import config
import json
from foundation_model import create_camel_model


from dotenv import load_dotenv

env_path = config.env_path
load_dotenv()

set_log_level(level="DEBUG")


def process_task_logging(workforce: Workforce, task: Task, log_dir: str) -> Task:
    """
    Run the `process_task` method of a Workforce instance and capture all logger outputs.

    Args:
        workforce (Workforce): The Workforce instance.
        task (Task): The task to be processed.
        log_dir (str): The directory to save the log file.

    Returns:
        Task: The updated task after processing.
    """
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, "meeting_detailed_actions.log")

    # Configure a FileHandler for the logger
    file_handler = logging.FileHandler(log_file_path, mode="w")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Add the FileHandler to the logger
    logger = logging.getLogger()  # Get the root logger
    logger.addHandler(file_handler)

    try:
        # Run the process_task method
        result_task = workforce.process_task(task)
    finally:
        # Remove the FileHandler after execution to avoid duplicate logs
        logger.removeHandler(file_handler)

    return result_task


def load_member_profile(
    member_profile_path: str,
    search_tools: list,
):
    with open(member_profile_path, "r") as f:
        member_profile = json.load(f)

    member_agent = ChatAgent(
        BaseMessage.make_assistant_message(
            role_name=member_profile["role"],
            content=f"""You are the {member_profile['role']} in a {config.company_type}.
            As a {member_profile['role']}, you are assigned to {member_profile['description']}.
            Your personality is {member_profile['personality']}.""",
        ),
        model=create_camel_model(),
        tools=[*search_tools],
    )
    return member_profile, member_agent


def WeeklyPlan(member_dir: str):
    search_toolkit = SearchToolkit()
    search_tools = [
        FunctionTool(search_toolkit.search_google),
        FunctionTool(search_toolkit.search_duckduckgo),
    ]

    agent_kwargs = {
        "model": create_camel_model(),
    }

    workforce = Workforce(
        "Meeting for weekly schedule",
        coordinator_agent_kwargs=agent_kwargs,
        task_agent_kwargs=agent_kwargs,
        new_worker_agent_kwargs=agent_kwargs,
    )

    all_roles = set()
    id_role_map = {}

    for file in os.listdir(member_dir):
        if file.endswith(".jsonc"):
            member_profile_path = os.path.join(member_dir, file)
            member_profile, member_agent = load_member_profile(
                member_profile_path,
                search_tools,
            )
            all_roles.add(member_profile["role"])  # add roles
            id_role_map[member_profile["id"]] = member_profile[
                "role"
            ]  # add id-role map
            member_description = f"{member_profile['role']}-{member_profile['name']}"
            workforce.add_single_agent_worker(member_description, worker=member_agent)

    # specify the task to be solved
    human_task = Task(
        content=f"""The company has {config.employee_number} employees with {len(all_roles)} type of roles:
        **{all_roles}**. The employee id and their role are as follows: {id_role_map}.
        The company is planning to have a meeting to discuss the weekly goals for each employee.
        The overall goal here is to settle plans for each employee for the next **{config.period}** weeks to **{config.goal}**.
        Everyone should actively participate in the discussion and have the detailed plan for each week.
        Every employee should have their own goals and tasks for each week, and they do not need to execute at this time.
        You should provide detailed expected goals for **each week for each member(agent)**.
        The output format should be as the pandas DataFrame with {config.employee_number} rows (for each member of the company) and {config.period+1} columns (for each week starting from Week1).
        Each cell should contain the detailed expected goals for each member for that week.""",
        # subtasks=[Task(content="The output format should be a table with 4 columns: Week, Developer, Designer, Product Manager. Each column should contain the expected goals for each role for that week.")],
        id="0",
    )

    log_dir = config.meeting_log_dir
    task_discuss = process_task_logging(workforce, human_task, log_dir)

    print("Final Result of Original task:\n", task_discuss.result)
    # save task_discuss.result to a file
    with open(os.path.join(log_dir, "meeting_result.log"), "w") as f:
        f.write(task_discuss.result)

    # move /data/meeting_logs/* to log_dir if the path exists
    meeting_logs_src = "/data/meeting_logs"
    if os.path.exists(meeting_logs_src):
        import shutil

        for item in os.listdir(meeting_logs_src):
            shutil.move(os.path.join(meeting_logs_src, item), log_dir)


if __name__ == "__main__":
    WeeklyPlan(
        member_dir=config.profile_output_dir,
    )
