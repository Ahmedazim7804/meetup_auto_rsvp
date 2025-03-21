from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Browser(ABC):
    name: str
    user_agent: str

    @abstractmethod
    def extract_cookies(self):
        pass