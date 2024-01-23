from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Callable


@dataclass
class Search(ABC):
    elements: List[Any] = field(default_factory=list)
    element_to_str: Callable = lambda element: str(element)
    is_stale: Callable = lambda element: False

    def __post_init__(self):
        for element in self.elements:
            self.process_element(element)

    def add_elements(self, elements: List[Any]):
        for element in elements:
            self.process_element(element)
        self.elements.extend(elements)

    def process_element(self, element: str):
        pass

    @abstractmethod
    def search(self) -> List[Any]:
        ...
