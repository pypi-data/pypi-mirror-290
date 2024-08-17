from unittest.mock import mock_open, patch

import pytest  # noqa: F401
from promptarchitect.engineered_prompt import EngineeredPrompt
from promptarchitect.log_error import Severity

# Sample prompt data to use in tests
valid_prompt_content = """
---
provider: openai
model: gpt-4o
key: value
output: output.txt
---
"""


# Define fixtures to use in your tests
@pytest.fixture
def valid_prompt_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "prompt.txt"
    p.write_text(valid_prompt_content)
    return p


def test_execute(valid_prompt_file):
    ep = EngineeredPrompt(prompt_file_path=str(valid_prompt_file))

    # Test with input_text
    response_text = ep.execute(
        input_text="What's the capital The Netherlands.", cached=False
    )

    assert "Amsterdam" in response_text


# Helper function to create a dummy EngineeredPrompt instance
def create_engineered_prompt():
    prompt_file_path = "dummy_prompt_file.json"
    output_path = "text"
    return EngineeredPrompt(prompt_file_path, output_path)


def test_read_from_input_file_success():
    ep = create_engineered_prompt()
    input_file = "test_input_file.txt"
    file_content = "This is a test file content."

    with patch("builtins.open", mock_open(read_data=file_content)):
        assert ep.read_from_input_file(input_file) == file_content


def test_read_from_input_file_not_found():
    ep = create_engineered_prompt()
    input_file = "non_existent_file.txt"

    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            ep.read_from_input_file(input_file)


def test_read_from_input_file_permission_denied():
    ep = create_engineered_prompt()
    input_file = "permission_denied_file.txt"

    with patch("builtins.open", side_effect=PermissionError):
        with pytest.raises(PermissionError):
            ep.read_from_input_file(input_file)


def test_execute_with_unreadable_input_file():
    ep = create_engineered_prompt()
    input_file = "unreadable_file.txt"

    with patch.object(ep, "read_from_input_file", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            ep.execute(input_file=input_file)
            last_error = ep.errors.errors[-1]
            assert "Error reading input file" in last_error["message"]
            assert last_error["severity"] == Severity.ERROR
