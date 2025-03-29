from dataclasses import dataclass
from src.enums import QueryMethod
from typing import Any, TypedDict

BaseHeaders = TypedDict(
        "BaseHeaders", {
            "Accept": str,
            "Referer": str,
            "baggage": str,
            "Origin": str,
            "Connection": str,
            "Priority": str,
            "User-Agent": str, "Accept-Language": str,
            'content-type': str,
            'apollographql-client-name': str,
            'x-meetup-view-id': str,
            'sentry-trace': str,
            'Sec-Fetch-Dest': str,
            'Sec-Fetch-Mode': str,
            'Sec-Fetch-Site': str,
            },
        total=False
    )