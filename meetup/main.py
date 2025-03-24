from http import client
import click
from models.group import Group
from client.meetup_client import Client
from queries.groups_query import GroupsQuery, GroupQueryParams
from queries.group_events_query import GroupEventsQuery, GroupEventsQueryParams
from queries.rsvp_event_query import RsvpEventQuery, RsvpEventQueryParams
from queries.get_event_with_id import EventQuery, EventQueryParams
from loguru import logger
from models.event import Event
from models.rsvp import Rsvp
from prettytable import PrettyTable

def get_groups() -> list[Group] | None:
    client = Client()
    groupsQuery = GroupsQuery(extraHeaders={}, extraCookies={}, params=GroupQueryParams())
    groups: list[Group] | None = client.executeQuery(query=groupsQuery)

    if groups == None:
        logger.error("No groups found")

    return groups

def get_group_events(group: Group) -> list[Event] | None:
    client = Client()
    groupEventQuery = GroupEventsQuery(extraHeaders={}, extraCookies={}, params=GroupEventsQueryParams(groupName=group.urlIdentifier))
    events: list[Event] | None = client.executeQuery(query=groupEventQuery)

    return events

def rsvp_event(event_id: str, venue_id: str, email_opt_in: bool = False) -> Rsvp | None:
    client = Client()
    rsvpQuery = RsvpEventQuery(extraCookies={}, extraHeaders={}, params=RsvpEventQueryParams(eventId=event_id, venueId=venue_id, emailOptIn=False))
    rsvp: Rsvp | None = client.executeQuery(rsvpQuery)

    return rsvp


@click.command(name="groups")
@click.help_option("--help", "-h")
def get_groups_command():
    """Get groups joined by the user"""
    groups: list[Group] | None = get_groups()

    if groups == None:
        click.echo("No groups found", err=True)
        return

    table = PrettyTable(["Serial No.", "id", "Name"])

    for sno, group in enumerate(groups, 1):
        table.add_row([sno, group.id, group.urlIdentifier])

    click.echo(table)

    return groups

@click.command(name="events")
@click.option("--group-id", "-g", help="Group id to get events", required=False)
@click.option("--all", "-i", help="Get events from all groups", required=False, is_flag=True)
def get_groups_events_command(group_id: str, all: bool, silent: bool = False):
    """Get events for a group"""

    click.echo(f"Group id: {group_id}")

    if group_id == None and all == False:
        click.echo("Either group-id or all should be provided", err=True)

    if group_id != None and all == True:
        click.echo("Only one of group-id or all should be provided", err=True)
    

    table = PrettyTable(["Serial No.", "id", "Title", "Time", "Venue", "Venue ID", "RSVP Open", "You are going"])
    groups: list[Group] | None = get_groups()

    if groups == None:
        click.echo("No groups found", err=True)
        return

    if group_id != None:
        click.echo(f"Getting events for group: {group_id}")
        group_with_given_id = next((group for group in groups if group.id == group_id), None)

        if group_with_given_id == None:
            click.echo(f"You are not part of any group with given id {group_id}", err=True)
            return
        
        events : list[Event] | None = get_group_events(group_with_given_id)

        if events == None:
            click.echo(f"No events found for group {group_with_given_id.urlIdentifier}", err=True)
            return

        for sno, event in enumerate(events, 1):
            table.add_row([sno, event.id, event.title, event.startTime, event.venue.name, event.venue.id, event.rsvpOpen, event.youGoing])

        click.echo(table)
        return events

    if all == True:
        for group in groups:
            click.echo(f"Getting events for group: {group.urlIdentifier}")
            events = get_group_events(group)

            for sno, event in enumerate(events, 1):
                table.add_row([sno, event.id, event.title, event.startTime, event.venue.name, event.venue.id, event.rsvpOpen, event.youGoing])

        click.echo(table)
        return events


@click.command(name="rsvp")
@click.option("--event-id", "-e", help="Event id to RSVP", required=False)
@click.option("--venue-id", "-v", help="Venue id to RSVP", required=False)
@click.option("--email-opt-in", "-o", help="Email opt in", required=False, default=False)
@click.option("--all", "-a", help="RSVP for all events", required=False, is_flag=True)
def rsvp_event_command(event_id: str, venue_id: str, email_opt_in: bool, all: bool):
    """RSVP for an event"""

    allInfoProvided = (event_id != None and venue_id != None )
    anyInfoProvided = (event_id != None or venue_id != None)

    import pdb
    pdb.set_trace()

    if (anyInfoProvided == False and all == False):
        click.echo("Either provide event info or rsvp to all events", err=True)
        return
    
    if (anyInfoProvided == True and all == True):
        click.echo("Either rsvp to all events or specific event", err=True)
        return
    
    if (anyInfoProvided == True and allInfoProvided == False):
        click.echo("Provide all event info", err=True)
        return
    
    
    if (allInfoProvided == True):
        rsvp : Rsvp | None = rsvp_event(event_id, venue_id, email_opt_in)

        if rsvp == None:
            click.echo("RSVP failed", err=True)
            return

        click.echo(f"RSVP status: {rsvp.status}")
        return rsvp
    else:
        groups: list[Group] | None = get_groups()

        if groups == None:
            click.echo("RSVP failed", err=True)
            return

        for group in groups:
            events = get_group_events(group)

            if events == None:
                click.echo("RSVP failed", err=True)
                return

            for event in events:
                rsvp = rsvp_event(event.id, event.venue.id, email_opt_in)
                logger.info(f"Succesfully RSVPed to event {event.title} showing at {event.startTime} at {event.venue.name}")



@click.group()
def main():
    pass

main.add_command(get_groups_command)
main.add_command(get_groups_events_command)
main.add_command(rsvp_event_command)

if __name__ == "__main__":
    main()
    # client = Client()

    # eventQuery = EventQuery(extraHeaders={}, extraCookies={}, params=EventQueryParams(event_id="306736069"))
    # client.executeQuery(query=eventQuery)
