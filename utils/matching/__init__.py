import json

import ollama

from .prompts import get_match_prompt
from ..types import IndustryCode, IndustryStandard
from ..inference.infer import get_children, get_common_parent, get_parent, select_cell

def query_llm(company, to_codes):
	prompt = get_match_prompt(company, to_codes)
	to_std = to_codes[0].std
	print("Prompt: " + prompt)

	response = ollama.generate(model='llama3', prompt=prompt, format="json", options={"temperature": 0.3})
	response = json.loads(response["response"])
	# print(f"Given {from_code.std.value} code: {from_code.value}, matched {to_std.value} code: {response[to_std.value]}")

	# return IndustryCode(to_std, "")
	return IndustryCode(to_std, response[to_std.value])

def get_match(company, to_codes):
	from_code = company.code
	to_std = to_codes[0].std
	# print(f"'{from_code.std.value}', '{from_code.value}', '{to_std.value}', '{to_guesses_str}'")

	if to_std == IndustryStandard.ISIC:
		return IndustryCode(IndustryStandard.ISIC, select_cell(from_code, "ISIC code"))

	if len(to_codes) == 0:
		# Find common parent
		common_parent = get_common_parent(from_code, to_std)
		match = common_parent

		while len(get_children(match)) > 0:
			to_codes = get_children(match)

			# If there is only one child, that is assumed to be the match
			if len(to_codes) == 1:
				match = to_codes[0]

			# If there are multiple children, 
			elif len(to_codes) > 1:
				match = query_llm(company, to_codes)

		return match

	elif len(to_codes) == 1:
		return to_codes[0]

	# print(f"Given {from_code.std.value} code: {from_code.value}, given {to_std.value} codes: {to_guesses_str}")
	return query_llm(company, to_codes)