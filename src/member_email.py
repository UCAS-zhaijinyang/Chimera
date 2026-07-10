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

import json5

import config
from foundation_model import run_llm
from json_utils import parse_llm_json

env_path = config.env_path
load_dotenv()


def get_email_members(activity, member_profile, member_id_list):
    for attempt in range(config.max_attempt):
        system_prompt = f"""Your name is {member_profile['name']} and you member id is {member_profile['id']}.
                                Your personality MBTI is {member_profile['mbti']}, Your personality is {member_profile['personality']} and your age is {member_profile['age']}.
                                You are the {member_profile['role']} in a {config.company_type}. The goal of your company is {config.goal}. \n\n
                                Now you are going to send an email to your colleagues to support your daily work.
                                The email is related to the following task: {activity}. \n\n
                                I will provide you with the member information list, and you will return the selected members for contact.
                                **Directly return a JSON array of member ids you should contact (do not include yourself). Example: ["da-1", "pc-1"]. Do not reply with anything else!**\n\n"""
        user_prompt = f"""The detailed members' information in the company is as follows: member_ids = {member_id_list}"""
        llm_output = run_llm(system_prompt, user_prompt)

        output = llm_output

        if isinstance(output, list):
            return output

        try:
            contact_members = parse_llm_json(output, expect=list)
            if not isinstance(contact_members, list):
                raise TypeError("contact members must be a list")
            break
        except Exception as e:
            print("[WARN] Error parsing JSON:", e, "Retrying...")
            if attempt == config.max_attempt - 1:
                print("[Error] Max attempts reached. Email sent to no one.")
                print(f"### Errored JSON ### : {output}")
                contact_members = []  # set to some default value to avoid crashing

    return contact_members


def get_email_content(activity, member_profile):
    for attempt in range(config.max_attempt):
        system_prompt = f"""Your name is {member_profile['name']}.
                                Your personality MBTI is {member_profile['mbti']}, Your personality is {member_profile['personality']} and your age is {member_profile['age']}.
                                You are the {member_profile['role']} in a {config.company_type} The goal of your company is {config.goal}. \n\n
                                Now you are going to send an email to your colleagues to support your daily work.
                                The email is related to the task you are working on, and I will provide you with the task details.\n\n
                                Please help me draft an email to finish your task based on your personality.
                                **Directly discuss the matter via email content and do not propose to have a meeting or discussion. You can detail to thoughts in the email content.**\n
                                **Please only reply with a JSON object with keys \"subject\" and \"content\". Escape newlines in content as \\n. Do not include markdown fences or any other text.** \n\n"""
        user_prompt = f"""The task is: {activity}"""
        llm_output = run_llm(system_prompt, user_prompt)
        output = llm_output

        try:
            email_content = parse_llm_json(output, expect=dict)
            if "subject" not in email_content or "content" not in email_content:
                raise KeyError("email JSON must contain subject and content")
            break
        except Exception as e:
            print("[WARN] Error parsing JSON:", e, "Retrying...")
            if attempt == config.max_attempt - 1:
                print("[Error] Max attempts reached. Using fallback email content.")
                print(f"### Errored JSON ### : {output}")
                email_content = {
                    "subject": f"Regarding: {activity[:80]}",
                    "content": (
                        output
                        if isinstance(output, str) and output.strip()
                        else f"Following up on: {activity}"
                    ),
                }

    return email_content


def reply_email_content(sender_id, incom_email_data, member_profile):
    for attempt in range(config.max_attempt):
        email_subject = incom_email_data["subject"]
        email_content = incom_email_data["content"]

        # read profile for the sender
        sender_profile_path = f"{config.profile_output_dir}/{sender_id}.jsonc"
        with open(sender_profile_path, "r") as f:
            sender_profile = json5.load(f)

        system_prompt = f"""Your name is {member_profile['name']}.
                                Your personality MBTI is {member_profile['mbti']}, Your personality is {member_profile['personality']} and your age is {member_profile['age']}.
                                You are the {member_profile['role']} in a {config.company_type}.
                                The goal of your company is {config.goal}. \n\n
                                Now you have received the email from your colleague {sender_profile['name']} with id of {sender_id}, who is the {sender_profile['role']} in your company.
                                I will provide you with the subject and the content of the email.\n\n
                                Now you can decide whether to reply to this email based on your judgment and your personality regarding whether the discussed issue has been resolved.
                                If you feel like the conversation in this email does not need further reaction, then directly return with \"No\", while if you want to reply, **Directly discuss the matter via email (in detail) and do not propose to have a meeting some time later**.
                                **You should detail to thoughts in the email content.** then return ONLY a JSON object with keys \"subject\" and \"content\". Escape newlines in content as \\n. Do not include markdown fences or any other text. \n\n"""
        user_prompt = f"The email subject is {email_subject} and the email content is {email_content}"
        llm_output = run_llm(system_prompt, user_prompt)
        output = llm_output

        if isinstance(output, str) and output.strip().startswith("No"):
            reply_content = {}
            return False, reply_content

        try:
            reply_content = parse_llm_json(output, expect=dict)
            if "subject" not in reply_content or "content" not in reply_content:
                print("[WARN] Invalid JSON format. Retrying...")
                if attempt == config.max_attempt - 1:
                    print(
                        "[Error] Max attempts reached. Skip reply to avoid crashing the day."
                    )
                    print(f"### Errored JSON ### : {output}")
                    return False, {}
            else:
                return True, reply_content
        except Exception as e:
            print("[WARN] Error parsing JSON:", e, "Retrying...")
            if attempt == config.max_attempt - 1:
                print(
                    "[Error] Max attempts reached. Skip reply to avoid crashing the day."
                )
                print(f"### Errored JSON ### : {output}")
                return False, {}

    return False, {}


if __name__ == "__main__":
    ###
    ### Test reply_email_content
    ###

    # email_data = {
    #     "from": "dev-1",
    #     "to": ["des-1", "dev-2"],
    #     "subject": "Regarding the front page design of the game and the game logo",
    #     "content": "Hi, I am Avery Lin, the developer of the game. I would like to ask you about the front page design of the game and the game logo. Could you please provide me with some information? Thank you!"
    # }
    email_data = {
        "from": "des-1",
        "to": ["dev-2"],
        "subject": "Re: Regarding the front page design of the game and the game logo",
        "content": "Hi, Please find the attach file as the design plan for the game. Thank you!",
    }
    reply_email, reply_content = reply_email_content(email_data)

    # activity = "contact @designer to ask regarding the front page design of the game and the game logo"
    # output = get_email_members(activity)
    # output = get_email_content(activity)
