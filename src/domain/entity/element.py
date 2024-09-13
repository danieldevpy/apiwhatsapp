from dataclasses import dataclass



@dataclass
class Element:
    name: str
    element_search: str
    type: None
    element_retry: None = None
    time: int = 5
