import click
from models.group import Group
from client.meetup_client import Client
from queries.groups_query import GroupsQuery, GroupQueryParams
from queries.group_events_query import GroupEventsQuery, GroupEventsQueryParams
from queries.rsvp_event_query import RsvpEventQuery, RsvpEventQueryParams
from loguru import logger
from models.event import Event
from models.rsvp import Rsvp
from prettytable import PrettyTable

def get_groups() -> list[Group]:
    client = Client()
    groupsQuery = GroupsQuery(extraHeaders={}, extraCookies={}, params=GroupQueryParams())
    groups: list[Group] = client.executeQuery(query=groupsQuery)

    return groups

def get_group_events(group: Group) -> list[Event]:
    client = Client()
    groupEventQuery = GroupEventsQuery(extraHeaders={}, extraCookies={}, params=GroupEventsQueryParams(groupName=group.urlIdentifier))
    events: list[Event] = client.executeQuery(query=groupEventQuery)

    return events

def rsvp_event(event: Event) -> Rsvp:
    client = Client()
    rsvpQuery = RsvpEventQuery(extraCookies={}, extraHeaders={}, params=RsvpEventQueryParams(eventId=event.id, venueId=event.venue.id, emailOptIn=False))
    rsvp: Rsvp = client.executeQuery(rsvpQuery)

    return rsvp


@click.command(name="groups")
@click.help_option("--help", "-h")
def get_groups_command():
    """Get groups joined by the user"""
    groups: list[Group] = get_groups()

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
    

    table = PrettyTable(["Serial No.", "id", "Title", "Time", "Venue", "RSVP Open"])
    groups: list[Group] = get_groups()

    if group_id != None:
        click.echo(f"Getting events for group: {group_id}")
        group_with_given_id = next((group for group in groups if group.id == group_id), None)

        if group_with_given_id == None:
            click.echo(f"You are not part of any group with given id {group_id}", err=True)
            return
        
        events = get_group_events(group_with_given_id)

        for sno, event in enumerate(events, 1):
            table.add_row([sno, event.id, event.title, event.startTime, event.venue.name, event.rsvpOpen])

        click.echo(table)
        return events

    if all == True:
        for group in groups:
            click.echo(f"Getting events for group: {group.urlIdentifier}")
            events = get_group_events(group)

            for sno, event in enumerate(events, 1):
                table.add_row([sno, event.id, event.title, event.startTime, event.venue.name, event.rsvpOpen])

        click.echo(table)
        return events


@click.command(name="rsvp")
@click.option("--event-id", "-e", help="Event id to RSVP", required=True)
@click.option("--venue-id", "-v", help="Venue id to RSVP", required=True)
@click.option("--email-opt-in", "-o", help="Email opt in", required=False, default=False)
@click.option("--all", "-i", help="RSVP for all events", required=False, is_flag=True)
def rsvp_event_command(event_id: str, venue_id: str, email_opt_in: bool):
    """RSVP for an event"""
    pass



@click.group()
def main():
    pass

main.add_command(get_groups_command)
main.add_command(get_groups_events_command)

if __name__ == "__main__":
    main()





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
