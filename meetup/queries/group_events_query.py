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
class GroupEventsQueryParams():
    groupName: str
    after: str | None = None


class GroupEventsQuery(BaseQuery):
    queryName = 'GroupEventsQuery'
    queryDesc = 'Query to get all events of a group'
    staticExtraHeaders = {}
    staticExtraCookies = {}
    staticParams = {
        'operationName': 'getUpcomingGroupEvents',
        'variables': {
            # 'urlname': 'travelingsoulsdotorg',
            # 'after': 'id of the last event',
            # 'afterDateTime': '2025-03-18T15:47:14.693Z',
        },
        'extensions': {
            'persistedQuery': {
                'version': 1,
                'sha256Hash': 'e1a588d73cb23d2cff73d5f6afa677d26e1e905835d084afb93ae5c456cc4812',
            },
        }
    }

    def __init__(self, extraHeaders: dict, extraCookies: dict, params: GroupEventsQueryParams):

        extraHeaders = {**self.staticExtraHeaders, **extraHeaders}
        extraCookies = {**self.staticExtraCookies, **extraCookies}

        self.staticParams['variables']['urlname'] = params.groupName
        self.staticParams['variables']['after'] = params.after
        self.staticParams['variables']['afterDateTime'] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

        finalParams = {**self.staticParams, **params.__dict__}

        super().__init__(method=QueryMethod.GET, url=BASE_GQL_URL, extraCookies=extraCookies, extraHeaders=extraHeaders, params=finalParams, queryName=self.queryName, queryDesc=self.queryDesc)
        

    def scrape(self, content: dict[str, Any]) -> list[Event]:

        logger.info(f"Scraping events from content received by {self.queryName}")

        eventsData = content['data']['groupByUrlname']['events']
        totalEvents = eventsData['totalCount']

        rawEvents : list[dict[str, Any]] = eventsData['edges']

        events: list[Event] = []

        for rawEvent in rawEvents:
            try:
                node = rawEvent['node']
                event = Event.from_json(node)
                events.append(event)
            except Exception as e:
                logger.error(f"Error parsing event: {e}")


        logger.info(f"Scraped {len(events)} events from {totalEvents} events")
        return events