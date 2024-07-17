import json

import ollama

from utils import LLM_ID, LLM_OPTIONS

def infer_json_from_llm(prompt: str) -> dict:
    """Infer a JSON response using a LLM.

    Args:
        prompt (str): Prompt provided to the LLM.

    Returns:
        dict: JSON response.
    """

    response = ollama.generate(model=LLM_ID, prompt=prompt, format="json", options=LLM_OPTIONS)
	# print(response)

    return json.loads(response["response"])