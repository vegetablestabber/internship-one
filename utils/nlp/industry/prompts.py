import re

from autocorrect import Speller

from utils.industry import Company, IndustryCode
from utils.inference.industry.infer import select_series

_spell = Speller()

def get_detailed_code_str(code: IndustryCode, autocorrect=False) -> str | None:
	"""Get a formatted string containing all information relevant to an industry classification.

	Args:
		code (IndustryCode): Code of the industry classification.
		autocorrect (bool, optional): Choose to autocorrect text. Defaults to False.

	Returns:
		str | None: Detailed description of the industry classification.
	"""

	series = select_series(code)
    
	if not series.empty:
		series = series[series.index[~series.index.isin(["Level", "Parent", "ISIC code"])]]
		string = f"{code.std.value} Code: {series.name}\n"

		for col in series.index:
			if series[col] != "":
				text = re.sub(r"\s*\(\d+\.\d+(?:\,\s*\d+\.\d+)*\)", "", series[col])
				text = text.replace("\n", "")
				
				string += f"{col}: {_spell(text) if autocorrect else text}\n"
						
		return string.strip()

	return None

def get_detailed_company_str(company: Company, autocorrect=False) -> str:
	"""Get a formatted string containing the description of a company.

	Args:
		company (Company): Company whose description to format.
		autocorrect (bool, optional): Choose to autocorrect the company description. Defaults to False.

	Returns:
		str: Description of the company's business.
	"""

	return f"Company description: {_spell(company.description) if autocorrect else company.description}\n{get_detailed_code_str(company.code)}"

def get_industry_match_prompt(company: Company, to_codes: list[IndustryCode]) -> str:
	"""Get a prompt to match a company to a list of suggested industry classifications.

	Args:
		company (Company): Company to be classified.
		to_codes (list[IndustryCode]): Suggested list of industry classification codes.

	Returns:
		str: Formatted prompt.
	"""

	from_std = company.code.std
	to_std = to_codes[0].std

	# prompt = f"Classify the company below given its {from_std.value} code and description to the most similar" \
	# 		 f" of the following {to_std.value} codes using their descriptions, examples and exclusions. When" \
	#    		 f" returning the result as JSON, the keys for the given code should be '{from_std.value}' and for" \
	# 		 f" the matched code as '{to_std.value}:\n\n{get_detailed_company_str(company)}"

	prompt = f"Classify the company below given its {from_std.value} code and description to the most similar" \
			 f" of the following {to_std.value} codes using their descriptions, examples and exclusions. Return" \
			 f" a JSON object with exactly two string key-value pairs: (1) key: '{from_std.value}', value: the given" \
			 f" {from_std.value} code, (2) key: '{to_std.value}', value: the matched {to_std.value} code. Do NOT" \
			 f" return any verbal information that was provided to assist in your task such as the description:" \
			 f"\n\n{get_detailed_company_str(company, autocorrect=True)}"

	for code in to_codes:
		prompt += "\n\n" + get_detailed_code_str(code)

	return prompt