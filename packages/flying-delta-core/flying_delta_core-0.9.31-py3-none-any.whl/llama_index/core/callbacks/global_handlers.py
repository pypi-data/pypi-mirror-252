"""Global eval handlers."""

from typing import Any

from llama_index.core.callbacks.base_handler import BaseCallbackHandler
from llama_index.core.callbacks.simple_llm_handler import SimpleLLMHandler


def set_global_handler(eval_mode: str, **eval_params: Any) -> None:
    """Set global eval handlers."""
    import llama_index

    llama_index.core.global_handler = create_global_handler(eval_mode, **eval_params)


def create_global_handler(eval_mode: str, **eval_params: Any) -> BaseCallbackHandler:
    """Get global eval handler."""
    return SimpleLLMHandler(**eval_params)
