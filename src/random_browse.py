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
import sys
import config

from camel.toolkits import (
    SearchToolkit,
    BrowserToolkit,
    FileWriteToolkit,
)
from camel.logger import set_log_level

from owl.utils import run_society

from camel.societies import RolePlaying
from foundation_model import create_camel_model

set_log_level(level="DEBUG")


def construct_society(question: str) -> RolePlaying:
    r"""Construct a society of agents based on the given question.

    Args:
        question (str): The task or question to be addressed by the society.

    Returns:
        RolePlaying: A configured society of agents ready to address the
            question.
    """

    models = {
        "user": create_camel_model(temperature=0),
        "assistant": create_camel_model(temperature=0),
        "browsing": create_camel_model(temperature=0),
        "planning": create_camel_model(temperature=0),
    }

    # Configure toolkits
    tools = [
        *FileWriteToolkit(output_dir="./").get_tools(),
    ]
    if not config.offline_mode:
        tools += [
            *BrowserToolkit(
                headless=True,
                web_agent_model=models["browsing"],
                planning_agent_model=models["planning"],
            ).get_tools(),
            SearchToolkit().search_duckduckgo,
            SearchToolkit().search_google,
            SearchToolkit().search_wiki,
        ]

    # Configure agent roles and parameters
    max_tool_iterations = getattr(config, "max_tool_iterations", 20)
    user_agent_kwargs = {
        "model": models["user"],
        "max_tool_iterations": max_tool_iterations,
    }
    assistant_agent_kwargs = {
        "model": models["assistant"],
        "tools": tools,
        "max_tool_iterations": max_tool_iterations,
    }

    # Configure task parameters
    task_kwargs = {
        "task_prompt": question,
        "with_task_specify": False,
    }

    # Create and return the society
    society = RolePlaying(
        **task_kwargs,
        user_role_name="user",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="assistant",
        assistant_agent_kwargs=assistant_agent_kwargs,
    )

    return society


def main():
    r"""Main function to run the OWL system with an example question."""
    # Default research question
    default_task = "Navigate to ttfish.cc, count the paper numbers has been published. No need to verify your answer."

    # Override default task if command line argument is provided
    task = sys.argv[1] if len(sys.argv) > 1 else default_task

    # Construct and run the society
    society = construct_society(task)
    answer, chat_history, token_count = run_society(society)

    # Output the result
    print(f"\033[94mAnswer: {answer}\033[0m")


if __name__ == "__main__":
    main()
