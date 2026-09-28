"""The context-window regression discovered during the real DeepSeek probe."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# Camel/OWL are intentionally installed by scripts/bootstrap.sh rather than
# as a lightweight unit-test dependency.  Keep the pure-Python test suite
# usable on developer machines without that optional runtime; CI images that
# install Camel still execute all three tests below.
pytest.importorskip(
    "camel",
    reason="Camel runtime is installed by scripts/bootstrap.sh for live planning tests",
)


def test_meeting_keeps_long_input_without_increasing_completion_budget(monkeypatch):
    import config
    from planning_runtime import create_meeting_model
    from camel.agents import ChatAgent
    from camel.messages import BaseMessage
    from camel.types import OpenAIBackendRole
    monkeypatch.setattr(config, "foundation_corp", "deepseek")
    monkeypatch.setattr(config, "foundation_model", "deepseek-chat")
    monkeypatch.setattr(config, "api_key", "offline-test-placeholder")
    monkeypatch.setattr(config, "llm_agent_max_tokens", 4096)
    model = create_meeting_model()
    agent = ChatAgent("Preserve the meeting input.", model=model)
    long_input = "meeting " * 6000
    agent.update_memory(BaseMessage.make_user_message("User", long_input), OpenAIBackendRole.USER)
    messages, tokens = agent.memory.get_context()
    assert tokens > 4096
    assert messages[-1]["content"] == long_input
    assert model.model_config_dict["max_tokens"] == 4096


@pytest.mark.parametrize("provider,model_name", [("openai", "gpt-4.1"), ("google", "gemini-2.0-flash")])
def test_meeting_uses_configured_model_and_credential(monkeypatch, provider, model_name):
    import config
    from camel.models import ModelFactory
    from planning_runtime import credentials, create_meeting_model
    monkeypatch.setattr(config, "foundation_corp", provider)
    monkeypatch.setattr(config, "foundation_model", model_name)
    monkeypatch.setattr(config, "api_key", "")
    monkeypatch.setenv("CHIMERA_PLANNING_API_KEY", "offline-placeholder")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(ModelFactory, "create", lambda **kwargs: kwargs)
    credentials()
    kwargs = create_meeting_model()
    assert kwargs["model_type"] == model_name
    assert kwargs["api_key"] == "offline-placeholder"
