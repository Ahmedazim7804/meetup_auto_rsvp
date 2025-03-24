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

@dataclass
class GroupQueryParams():
    pass


class GroupsQuery(BaseQuery):
    queryName = 'GroupQuery'
    queryDesc = 'Query to get groups joined by the user'
    staticExtraHeaders = {}
    staticExtraCookies = {}
    staticParams = {
        'operationName': 'getSelfActiveGroups',
        'variables': {
            'first': 20,
        },
        'extensions': {
            'persistedQuery': {
                'version': 1,
                'sha256Hash': '40c4a04c8466f43b2b5719d8b7b8107b2f333b8b503a503b3ad43c7e41fb6b42',
            },
        },
    }

    def __init__(self, extraHeaders: dict, extraCookies: dict, params: GroupQueryParams):

        extraHeaders = {**self.staticExtraHeaders, **extraHeaders}
        extraCookies = {**self.staticExtraCookies, **extraCookies}
        finalParams = {**self.staticParams, **params.__dict__}

        super().__init__(method=QueryMethod.GET, url=BASE_GQL_URL, extraCookies=extraCookies, extraHeaders=extraHeaders, params=finalParams, queryName=self.queryName, queryDesc=self.queryDesc)
        

    def scrape(self, content: dict) -> list[Group]:

        logger.info(f"Scraping groups from content received by {self.queryName}")

        edges = content.get('data', {}).get('self', {}).get('memberships', {}).get('edges', None)

        if edges is None:
            logger.error(f"No groups found in content received by {self.queryName}")
            raise Exception("No groups found")
    
        if edges.__len__ == 0:
            logger.error(f"User has not joined any groups")

        groups : list[Group] = []

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
                organizerId=organizer.get('id', None) if organizer is not None else None,
                state=node.get('state', None),
                timezone=node.get('timezone', None),
                groupPhoto=groupPhoto
            )

            groups.append(group)

            logger.debug(f"Group scraped: {group.name}")

        return groups

