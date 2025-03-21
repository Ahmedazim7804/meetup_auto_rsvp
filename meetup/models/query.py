from dataclasses import dataclass
from enums import QueryMethod
from abc import ABC, abstractmethod


@dataclass
class BaseQuery(ABC):
    queryName: str
    queryDesc: str
    method: QueryMethod
    url: str
    extraHeaders: dict | None = None
    extraCookies: dict | None = None
    params: dict | None = None

    @abstractmethod
    def scrape(self, content: str) -> any:
        pass
    
