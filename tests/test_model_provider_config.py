import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_chat_completions_endpoint_is_normalized_to_openai_base_url():
    sys.path.insert(0, str(ROOT / "src"))
    from config import normalize_openai_compatible_base_url

    assert normalize_openai_compatible_base_url(
        "http://192.168.21.240/v1/chat/completions"
    ) == "http://192.168.21.240/v1"
    assert normalize_openai_compatible_base_url(
        "http://192.168.21.240/v1/"
    ) == "http://192.168.21.240/v1"


def test_glm_environment_selects_openai_compatible_provider_without_echoing_key():
    env = os.environ.copy()
    env.update(
        {
            "PYTHONPATH": str(ROOT / "src"),
            "GLM_ENDPOINT": "http://192.168.21.240/v1/chat/completions",
            "GLM_MODEL_ID": "GLM-5.3",
            "GLM_API_KEY": "test-glm-key",
        }
    )
    env.pop("LLM_BASE_URL", None)
    env.pop("LLM_MODEL_ID", None)
    env.pop("LLM_API_KEY", None)
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import config, json; print(json.dumps({"
                "'corp': config.foundation_corp,"
                "'model': config.foundation_model,"
                "'base_url': config.llm_base_url,"
                "'api_key': config.api_key}))"
            ),
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    settings = json.loads(result.stdout)
    assert settings == {
        "corp": "openai_compatible",
        "model": "GLM-5.3",
        "base_url": "http://192.168.21.240/v1",
        "api_key": "test-glm-key",
    }
