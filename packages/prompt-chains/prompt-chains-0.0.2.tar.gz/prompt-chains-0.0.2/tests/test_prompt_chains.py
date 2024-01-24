import pytest

from llm.prompt_chains.prompt_chains import prompt_chains


def test_prompt_chains():
    with pytest.raises(TypeError):
        prompt_chains()


