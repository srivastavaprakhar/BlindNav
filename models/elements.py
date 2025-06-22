from typing import List, Dict
from pydantic import BaseModel

class PageElements(BaseModel):
    headings: List[str]
    buttons: List[Dict[str, str]]
    links: List[Dict[str, str]]
    inputs: List[Dict[str, str]]
    forms: List[str]
