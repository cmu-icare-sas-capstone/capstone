from typing import List
import re


def match_all_values_by_wildcard(values: List[str], wildcard: str) -> List[str]:
    matched_values = []
    wildcard = "^" + wildcard + "$"
    for v in values:
        if type(v) != str:
            v = str(v)
        if re.match(wildcard.lower(), v.lower()):
            matched_values.append(v)

    return matched_values
