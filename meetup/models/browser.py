from dataclasses import dataclass
from abc import ABC, abstractmethod
from http.cookiejar import CookieJar
from typing import Any

@dataclass
class Browser(ABC):
    name: str
    user_agent: str

    @abstractmethod
    def extract_cookies(self) -> CookieJar:
        pass