
from models.query import BaseQuery
from typing import Any, TypedDict
from constants import BASE_GQL_URL
from urllib.parse import urljoin
from models.headers import BaseHeaders
from dataclasses import dataclass
from enums import QueryMethod
from loguru import logger
from models.rsvp import Rsvp
from models.event import Event
import json
import datetime as dt

@dataclass
class RsvpEventQueryParams():
    eventId: str
    venueId: str | None
    emailOptIn : bool = False


class RsvpEventQuery(BaseQuery):
    queryName = 'RsvpEventQuery'
    queryDesc = 'Query to RSVP to an event'
    staticExtraHeaders = {}
    staticExtraCookies = {}
    staticParams = {
        "operationName":"rsvpToEvent",
        "variables":{
            "input":
                {
                    # "eventId":"306736069",
                    "response":"YES",
                    # "proEmailShareOptin":False,
                    # "venueId":"27720082",
                    "eventPromotionId":"0"
                }
        },
        "extensions": {
            "persistedQuery":
                {
                    "version": 1,
                    "sha256Hash": "104ad391d9c74a112d21a4a926db31bb10c6087b9f93e86e7575f004857550ce"
                }
            }
        }

    def __init__(self, extraHeaders: dict, extraCookies: dict, params: RsvpEventQueryParams):

        extraHeaders = {**self.staticExtraHeaders, **extraHeaders}
        extraCookies = {**self.staticExtraCookies, **extraCookies}

        self.staticParams['variables']['input']['eventId'] = params.eventId
        self.staticParams['variables']['input']['venueId'] = params.venueId
        self.staticParams['variables']['input']['proEmailShareOptin'] = 'true' if params.emailOptIn else 'false'

        finalParams = {**self.staticParams, **params.__dict__}

        super().__init__(method=QueryMethod.GET, url=BASE_GQL_URL, extraCookies=extraCookies, extraHeaders=extraHeaders, params=finalParams, queryName=self.queryName, queryDesc=self.queryDesc)
        

    def scrape(self, content: dict[str, Any]) -> Rsvp:

        logger.info(f"Parsing RSVP response from {self.queryName}")

        rsvpData = content.get('data', {}).get('rsvp', None)

        if rsvpData['errors'] is not None:
            logger.error(f"Failed to RSVP because: {rsvpData['errors'][0]['message']}")
            raise Exception(f"Error in RSVP: {rsvpData['errors'][0]['message']}")

        if rsvpData is None or rsvpData.get('rsvp', None) is None:
            logger.error(f"Failed to RSVP beacuse No RSVP data found in content received by {self.queryName}")
            raise Exception(f"No RSVP data found in content received by {self.queryName}")
    

        rsvp = Rsvp.from_json(rsvpData['rsvp'])

        return rsvp

