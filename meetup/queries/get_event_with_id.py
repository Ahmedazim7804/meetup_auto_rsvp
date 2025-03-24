from models.query import BaseQuery
from typing import Any, TypedDict
from constants import BASE_GQL_URL
from urllib.parse import urljoin
from models.headers import BaseHeaders
from dataclasses import dataclass
from enums import QueryMethod
from loguru import logger
from models.group import Group
from models.event import Event
import json
import datetime as dt

@dataclass
class EventQueryParams():
    event_id: str


class EventQuery(BaseQuery):
    queryName = 'EventQuery'
    queryDesc = 'Query to get an event by id'
    staticExtraHeaders = {}
    staticExtraCookies = {}
    staticParams = {
        'operationName': 'getEventByIdForAttendees',
        'variables': {
            # 'eventId': '306736069',
            'first': 1,
            'filter': {
                'rsvpStatus': [
                    'YES',
                    'ATTENDED',
                ],
            },
            'sort': {
                'sortField': 'SHARED_GROUPS',
                'sortOrder': 'DESC',
                'hostsFirst': True,
            },
        },
        'extensions': {
            'persistedQuery': {
                'version': 1,
                'sha256Hash': '9c61aaab3afd4f2aba0533bcd4c1d00e31613425f6cf2d9cfa109689da5ebedf',
            },
        },
    }

    def __init__(self, extraHeaders: dict, extraCookies: dict, params: EventQueryParams):

        extraHeaders = {**self.staticExtraHeaders, **extraHeaders}
        extraCookies = {**self.staticExtraCookies, **extraCookies}

        self.staticParams['variables']['eventId'] = params.event_id

        finalParams = {**self.staticParams, **params.__dict__}

        super().__init__(method=QueryMethod.GET, url=BASE_GQL_URL, extraCookies=extraCookies, extraHeaders=extraHeaders, params=finalParams, queryName=self.queryName, queryDesc=self.queryDesc)

    def scrape(self, content: dict[str, Any]) -> Event:

        logger.debug(f"Scraping event data from content received by {self.queryName}")

        rawEventData = content['data']['event']
        event = Event.from_json(rawEventData)

        return event

