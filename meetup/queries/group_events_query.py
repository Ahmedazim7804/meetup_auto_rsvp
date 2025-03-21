from models.query import BaseQuery
from typing import TypedDict
from constants import BASE_GQL_URL
from urllib.parse import urljoin
from models.headers import BaseHeaders
from dataclasses import dataclass
from enums import QueryMethod
from loguru import logger
from models.group import Group
import json
import datetime as dt

@dataclass
class GroupEventsQueryParams():
    groupName: str
    after: str | None


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

    def __init__(self, extraHeaders: BaseHeaders, extraCookies: dict, params: GroupEventsQueryParams):

        extraHeaders = {**self.staticExtraHeaders, **extraHeaders}
        extraCookies = {**self.staticExtraCookies, **extraCookies}

        self.staticParams['variables']['urlname'] = params.groupName
        self.staticParams['variables']['after'] = params.after
        self.staticParams['variables']['afterDateTime'] = dt.now(dt.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

        params = {**self.staticParams}

        super().__init__(method=QueryMethod.GET, url=BASE_GQL_URL, extraCookies=extraCookies, extraHeaders=extraHeaders, params=params, queryName=self.queryName, queryDesc=self.queryDesc)
        

    def scrape(self, content: dict[str, any]) -> any:

        # content = json.loads(content)
        print(content)
        return

        logger.info(f"Scraping groups from content received by {self.queryName}")

        edges = content.get('data', {}).get('self', {}).get('memberships', {}).get('edges', None)

        if edges is None:
            logger.error(f"No groups found in content received by {self.queryName}")
            raise Exception("No groups found")
    
        if edges.__len__ == 0:
            logger.error(f"User has not joined any groups")

        for edge in edges:
            node = edge.get('node', None)
            organizer = node.get('organizer', None)

            if node is None:
                logger.error(f"Group has no information")
                
            if organizer is None:
                logger.error(f"Group has no organizer")
            
            groupPhoto = None
            if 'groupPhoto' in node:
                groupPhoto = node['groupPhoto']['baseUrl'] + node['groupPhoto']['id']

            group = Group(
                id=node['id'],
                city=node['city'],
                country=node['country'],
                link=node['link'],
                name=node['name'],
                urlIdentifier=node['urlname'],
                organizerId=organizer['id'],
                state=node.get('state', None),
                timezone=node.get('timezone', None),
                groupPhoto=groupPhoto
            )

            logger.debug(f"Group scraped: {group.name}")

