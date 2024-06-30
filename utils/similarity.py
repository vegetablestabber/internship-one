from .types import IndustryStandard, IndustryCode
from .constants import DIFF_THRESHOLD

# Obtain column name for similarity score, given ICS and company role
get_similarity_col = lambda std: f"{std.value} code sim. score"

# ASSUMPTION: If the difference of codes of the same level is within a given threshold, then they are equal.

# Ensure the strings are of comparable length
def comparable_codes(lst: list[IndustryCode]):
    min_len = min([len(code.value) for code in lst])
    return [IndustryCode(code.std, code.value[:min_len]) for code in lst]

# Compare two codes
def compare(code1: IndustryCode, code2: IndustryCode):
    if code1 != code2:
        if code1.value[0] != code2.value[0]:
            diff = abs(int(code1.value) - int(code2.value))
            return 1 if diff <= DIFF_THRESHOLD else 0

        # print("{0:<4} {1:>5} <-> {2:<4} {3:>5}".format(code1.std.value, code1.value, code2.std.value, code2.value))
    
    # if code1 != code2:
    #     diff = abs(int(code1.value) - int(code2.value))
    #     return 1 if diff <= DIFF_THRESHOLD else 0
    
    return 1

# Compare a code with a list of codes
def compare_one_to_many(code1: IndustryCode, codes):
    codes = comparable_codes([code1, *codes])[1:]
    scores = [compare(code1, code) for code in codes]
    
    return str(sum(scores) / len(scores))

# Compare a list of codes with another list of codes
def compare_many(codes1, codes2):
    lst = [comparable_codes([code1, code2]) for code1, code2 in zip(codes1, codes2)]
    lst = [tuple(l) for l in lst]
    
    scores = [compare(code1, code2) for code1, code2 in lst]
    return str(sum(scores) / len(scores))

# Split the text by either ';' or ','
def str_to_codes(str, std):
    if ";" in str:
        return [IndustryCode(std, substr) for substr in str.split(";")]
    elif "," in str:
        return [IndustryCode(std, substr) for substr in str.split(",")]
    
    return [IndustryCode(std, str)]

# Evaluate similarity score based on NACE code and another standard code
def get_similarity(code_str1: str, std1, code_str2: str, std2: IndustryStandard):
    code_str1 = code_str1.strip()
    code_str2 = code_str2.strip()

    blacklist = ["", "-"]
    # print(f"String 1: {code_str1} ({std1.value}), String 2: {code_str2} ({std2.value})")
    
    # If code does not exist
    if code_str1 in blacklist or code_str2 in blacklist:
        return 0
 
    std1_codes = str_to_codes(code_str1, std1)
    std2_codes = str_to_codes(code_str2, std2)
    
    if len(std1_codes) == len(std2_codes):
        return compare_many(std1_codes, std2_codes)
    elif len(std1_codes) > 1 and len(std2_codes) == 1:
        return compare_one_to_many(std2_codes[0], std1_codes)
    elif len(std1_codes) == 1 and len(std2_codes) > 1:
        return compare_one_to_many(std1_codes[0], std2_codes)
    
    return ""