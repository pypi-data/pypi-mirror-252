from typing import Dict, TypedDict

class CookieRequest(TypedDict):
    payload: Dict[str, str]
    headers: Dict[str, str]
    url: str