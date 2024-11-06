from typing import Annotated, Any, List, Dict
from typing_extensions import TypedDict
import operator

class State(TypedDict):
    status: str
    error: str
    requirements: str
    products: List[Dict[str, Any]]
    items: List[Dict[str, Any]]
