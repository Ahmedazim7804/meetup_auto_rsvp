import click
from models.query import BaseQuery
from client.meetup_client import Client
from enums import QueryMethod

from queries.groups_query import GroupsQuery, GroupQueryParams
from queries.group_events_query import GroupEventsQuery, GroupEventsQueryParams
from queries.rsvp_event_query import RsvpEventQuery, RsvpEventQueryParams
from loguru import logger
from models.event import Event
from models.rsvp import Rsvp

def get_groups():
    client = Client()

    groupsQuery = GroupsQuery(extraHeaders={}, extraCookies={}, params=GroupQueryParams())

    groups = client.executeQuery(query=groupsQuery)
    print(groups)


get_groups()




# client = Client()

# groupsQuery = GroupsQuery(extraHeaders={}, extraCookies={}, params=GroupQueryParams())

# groups = client.executeQuery(query=groupsQuery)

# for group in groups:
#     groupEventsQuery = GroupEventsQuery(extraHeaders={}, extraCookies={}, params=GroupEventsQueryParams(groupName=group.urlIdentifier))
#     logger.info(f"Getting events for group: {group.name}")
#     events: list[Event] = client.executeQuery(query=groupEventsQuery)

#     for event in events:
#         print(event.title)
#         rsvpQuery = RsvpEventQuery(extraCookies={}, extraHeaders={}, params=RsvpEventQueryParams(eventId=event.id, venueId=event.venue.id, emailOptIn=False))
#         rsvp: Rsvp = client.executeQuery(rsvpQuery)
