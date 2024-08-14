from typing import Dict, List


def get_text(fields: Dict, key: str) -> str:
    return fields[key][0]["text"]

def get_link_ids(fields: Dict, key: str) -> List[str]:
    return fields[key]["link_record_ids"]

