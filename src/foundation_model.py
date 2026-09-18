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
import config

from openai import OpenAI
from dotenv import load_dotenv

from google import genai
from google.genai import types

env_path = config.env_path
load_dotenv()


def _openai_compatible_kwargs():
    return {
        "api_key": config.api_key or "EMPTY",
        "base_url": config.llm_base_url,
    }


def _run_llm_max_tokens():
    return config.llm_max_tokens


def _qwen3_no_think_extra_body():
    """Disable Qwen3 thinking so structured JSON outputs stay parseable."""
    model = (config.foundation_model or "").lower()
    if "qwen3" not in model:
        return None
    return {
        "enable_thinking": False,
        "chat_template_kwargs": {"enable_thinking": False},
    }


def camel_model_backend_kwargs():
    """Shared kwargs for camel.models.ModelFactory.create."""
    from camel.types import ModelPlatformType, ModelType

    corp_to_type = {
        "openai": ModelType.GPT_4O_MINI,
        "google": ModelType.GEMINI_2_0_FLASH,
        "deepseek": ModelType.DEEPSEEK_CHAT,
        "openai_compatible": config.foundation_model,
    }
    corp_to_platform = {
        "openai": ModelPlatformType.OPENAI,
        "google": ModelPlatformType.GEMINI,
        "deepseek": ModelPlatformType.DEEPSEEK,
        "openai_compatible": ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    }
    kwargs = {
        "model_platform": corp_to_platform.get(
            config.foundation_corp, ModelPlatformType.DEFAULT
        ),
        "model_type": corp_to_type.get(
            config.foundation_corp, ModelType.GPT_4O_MINI
        ),
    }
    if config.foundation_corp == "openai_compatible":
        kwargs["url"] = config.llm_base_url
        kwargs["api_key"] = config.api_key or "EMPTY"
    elif getattr(config, "api_key", ""):
        kwargs["api_key"] = config.api_key
    return kwargs


def create_meeting_camel_model():
    from camel.models import ModelFactory

    kwargs = camel_model_backend_kwargs()
    model_config_dict = {
        "max_tokens": config.llm_agent_max_tokens,
        "tool_choice": "none",
    }
    extra_body = _qwen3_no_think_extra_body()
    if extra_body:
        model_config_dict["extra_body"] = extra_body
    kwargs["model_config_dict"] = model_config_dict
    return ModelFactory.create(**kwargs)


def create_camel_model(temperature=None):
    from camel.models import ModelFactory

    kwargs = camel_model_backend_kwargs()
    model_config_dict = {"max_tokens": config.llm_agent_max_tokens}
    if temperature is not None:
        model_config_dict["temperature"] = temperature
    if config.foundation_corp == "openai_compatible" and getattr(
        config, "local_llm_disable_tools", False
    ):
        model_config_dict["tool_choice"] = "none"
    extra_body = _qwen3_no_think_extra_body()
    if extra_body:
        model_config_dict["extra_body"] = extra_body
    if model_config_dict:
        kwargs["model_config_dict"] = model_config_dict
    return ModelFactory.create(**kwargs)


def run_llm(system_prompt, user_prompt, temperature=0):
    if config.foundation_corp == "openai":
        client = OpenAI()
        response = client.chat.completions.create(
            model=config.foundation_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            top_p=0.9,
            max_tokens=_run_llm_max_tokens(),
        )
        llm_output = response.choices[0].message.content

    elif config.foundation_corp == "google":
        client = genai.Client(api_key=config.api_key)
        response = client.models.generate_content(
            model=config.foundation_model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
                top_p=0.9,
                max_output_tokens=_run_llm_max_tokens(),
            ),
        )
        llm_output = response.text

    elif config.foundation_corp == "deepseek":
        client = OpenAI(api_key=config.api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model=config.foundation_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            top_p=0.9,
            max_tokens=_run_llm_max_tokens(),
            stream=False,
        )
        llm_output = response.choices[0].message.content

    elif config.foundation_corp == "xai":
        client = OpenAI(api_key=config.api_key, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model=config.foundation_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            top_p=0.9,
            max_tokens=_run_llm_max_tokens(),
            stream=False,
        )
        llm_output = response.choices[0].message.content

    elif config.foundation_corp == "openai_compatible":
        client = OpenAI(**_openai_compatible_kwargs())
        create_kwargs = dict(
            model=config.foundation_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            top_p=0.9,
            max_tokens=_run_llm_max_tokens(),
            stream=False,
        )
        extra_body = _qwen3_no_think_extra_body()
        if extra_body:
            create_kwargs["extra_body"] = extra_body
        response = client.chat.completions.create(**create_kwargs)
        llm_output = response.choices[0].message.content

    else:
        raise ValueError(
            "Invalid foundation_corp. Please choose from 'openai', 'google', "
            "'deepseek', 'xai', or 'openai_compatible'."
        )
    return llm_output
