import json

import ollama

from utils.industry import IndustryCode, IndustryStandard
from utils.inference.industry.infer import get_children, get_common_parent, select_cell

from .prompts import get_match_prompt

_options = {"temperature": 0.2, "top_k": 10, "top_p": 0.5}

def query_llm(company, to_std, guesses):
	prompt = get_match_prompt(company, guesses)
	# print("Prompt: " + prompt)

	response = ollama.generate(model='llama3', prompt=prompt, format="json", options=_options)
	response = json.loads(response["response"])
	# print(response)
	# print(f"Given {from_code.std.value} code: {from_code.value}, matched {to_std.value} code: {response[to_std.value]}")

	return IndustryCode(to_std, str(response[to_std.value]))

def get_match(company, to_std, guesses):
	from_code = company.code
	# print(f"'{from_code.std.value}', '{from_code.value}', '{to_std.value}', '{[c.value for c in guesses]}'")

	if to_std == IndustryStandard.ISIC:
		return IndustryCode(IndustryStandard.ISIC, select_cell(from_code, "ISIC code"))

	if len(guesses) == 0:
		# Find common parent
		common_parent = get_common_parent(from_code, to_std)
		match = common_parent

		while len(get_children(match)) > 0:
			guesses = get_children(match)

			# If there is only one child, that is assumed to be the match
			if len(guesses) == 1:
				match = guesses[0]

			# If there are multiple children, 
			elif len(guesses) > 1:
				match = query_llm(company, to_std, guesses)

		return match

	elif len(guesses) == 1:
		return guesses[0]

	# print(f"Given {from_code.std.value} code: {from_code.value}, given {to_std.value} codes: {to_guesses_str}")
	return query_llm(company, to_std, guesses)