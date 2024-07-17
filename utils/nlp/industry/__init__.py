from utils.industry import Company, IndustryCode, IndustryStandard

from .. import infer_json_from_llm
from .prompts import get_match_prompt

def infer_industry_code_from_llm(company: Company, to_std: IndustryStandard, guesses: list[IndustryCode]) -> IndustryCode:
	"""Infer an industry classification for a company using a LLM.

	Args:
		company (Company): Company to be classified.
		to_std (IndustryStandard): The industry classification standard to classify the company.
		guesses (list[IndustryCode]): Suggested list of industry classification codes.

	Returns:
		IndustryCode: Code of the inferred industry classification from the standard provided.
	"""

	prompt = get_match_prompt(company, guesses)
	# print("Prompt: " + prompt)

	response = infer_json_from_llm(prompt)
	# print(response)
	
	# Example response:
	# {
	#     "NACE": "2221",
	#     "WZ"  : "22210"
	# }

	return IndustryCode(to_std, str(response[to_std.value]))