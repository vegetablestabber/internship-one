import json

import ollama

_options = {"temperature": 0.2, "top_k": 10, "top_p": 0.5}
"""LLM parameters."""

def infer_json_from_llm(prompt: str) -> dict:
    """Infer a JSON response using a LLM.

    Args:
        prompt (str): Prompt provided to the LLM.

    Returns:
        dict: JSON response.
    """

    response = ollama.generate(model='llama3', prompt=prompt, format="json", options=_options)
	# print(response)

    return json.loads(response["response"])