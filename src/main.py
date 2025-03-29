import sys
import click
from src.config import MeetupConfig
from src.models.group import Group
from src.client.meetup_client import Client
from src.queries.groups_query import GroupsQuery, GroupQueryParams
from src.queries.group_events_query import GroupEventsQuery, GroupEventsQueryParams
from src.queries.rsvp_event_query import RsvpEventQuery, RsvpEventQueryParams
from src.queries.get_event_with_id import EventQuery, EventQueryParams
from loguru import logger
from src.models.event import Event, EventRsvpConditions
from src.models.rsvp import Rsvp
from prettytable import PrettyTable

config = MeetupConfig()

def get_groups() -> list[Group] | None:
    client = Client()
    groupsQuery = GroupsQuery(extraHeaders={}, extraCookies={}, params=GroupQueryParams())
    groups: list[Group] | None = client.executeQuery(query=groupsQuery)

    if groups == None:
        logger.warning("No groups found")

    return groups

def get_group_events(group: Group) -> list[Event] | None:
    client = Client()
    groupEventQuery = GroupEventsQuery(extraHeaders={}, extraCookies={}, params=GroupEventsQueryParams(groupName=group.urlIdentifier))
    events: list[Event] | None = client.executeQuery(query=groupEventQuery)

    return events

def rsvp_event(event_id: str, venue_id: str | None, email_opt_in: bool = False) -> Rsvp | None:
    client = Client()
    rsvpQuery = RsvpEventQuery(extraCookies={}, extraHeaders={}, params=RsvpEventQueryParams(eventId=event_id, venueId=venue_id, emailOptIn=False))
    rsvp: Rsvp | None = client.executeQuery(rsvpQuery)

    return rsvp


def config_groups():
    groups: list[Group] | None = get_groups()

    if groups == None:
        click.echo("No groups found, You must be part of atleast one group to use this application", err=True)
        return

    table = PrettyTable(["Serial No.", "id", "Name", "Identifier", "URL", "Selected"])

    for sno, group in enumerate(groups, 1):
        table.add_row([sno, group.id, group.name, group.urlIdentifier, group.link, "Yes" if group.id in config.groups else "No"])
    
    click.echo(table)

    click.echo("Select groups to Auto RSVP to events from")

    while True:
        try:
            user_input = click.prompt("Enter groups serial numbers separated by comma")

            raw_selected_groups = user_input.strip().replace(" ", "").replace("\t", "").split(",")
            selected_groups = [groups[int(group_id) - 1] for group_id in raw_selected_groups]

            if len(selected_groups) == 0:
                click.echo("Select atleast one group", err=True)
                continue

            click.echo(f"Selected groups: {[group.name for group in selected_groups]}")

            selected_groups_ids = [str(group.id) for group in selected_groups]

            config.groups = selected_groups_ids
            config.save()
            click.prompt("Config saved, press enter to continue")
            break

        except ValueError:
            click.echo("Invalid group id", err=True)
            continue
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            click.prompt("Press enter to continue")
            break;


def config_rsvp_conditions():
    click.clear()
    click.echo("Update condition for an event to Auto RSVP to")

    while True:
        click.echo("\n")
        config.save()

        click.echo("1. Auto RSVP to online events too")
        click.echo("2. Auto RSVP to events only if atleast this many attendees are going")
        click.echo("3. Auto RSVP to paid events too")
        click.echo("4. Exit")

        choice = click.prompt("Select condition to modify").strip().replace(" ", "").replace("\t", "")
            
        if choice == "1":

            value = click.prompt("Auto RSVP to online events? (y/n)").strip().replace(" ", "").replace("\t", "")
            if value == "y":
                config.conditions.isOnline = True
            elif value == "n":
                config.conditions.isOnline = False
            else:
                click.echo("Invalid choice", err=True)

        elif choice == "2":
            value = click.prompt("Minimum attendees required to Auto RSVP (number)").strip().replace(" ", "").replace("\t", "")

            try:
                value = int(value)
                config.conditions.minNumAttendees = value
            except ValueError:
                click.echo("Invalid number", err=True)


        elif choice == "3":
            value = click.prompt("Auto RSVP to paid events? (y/n)").strip().replace(" ", "").replace("\t", "")
            if value == "y":
                config.conditions.isPaid = True
            elif value == "n":
                config.conditions.isPaid = False
            else:
                click.echo("Invalid choice", err=True)
        elif choice == "4":
            break
        else:
            click.echo("Invalid choice", err=True)
            break


@click.command(name="config")
def config_command():
    """Update/Create meetup config"""

    while True:
        click.echo("1. Select groups to Auto RSVP to events from")
        click.echo("2. Update condition for an event to Auto RSVP to")
        click.echo("3. Exit")

        choice = click.prompt("Enter choice").strip().replace(" ", "").replace("\t", "")
        click.clear()

        if choice == "1":
            config_groups()
        elif choice == "2":
            config_rsvp_conditions()
        elif choice == "3" or choice == "exit" or choice == "q":
            break
        else:
            click.echo("Invalid choice", err=True)
            return
        
        click.clear()


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
            table.add_row([sno, event.id, event.title, event.startTime, getattr(event.venue, "name", "Online"), getattr(event.venue, 'id', "None"), event.rsvpOpen, event.youGoing])

        click.echo(table)
        return events

    if all == True:
        for group in groups:
            click.echo(f"Getting events for group: {group.urlIdentifier}")
            events = get_group_events(group)

            for sno, event in enumerate(events, 1):
                table.add_row([sno, event.id, event.title, event.startTime, getattr(event.venue, "name", "Online"), getattr(event.venue, 'id', "None"), event.rsvpOpen, event.youGoing])

        click.echo(table)
        return events


@click.command(name="rsvp")
@click.option("--email-opt-in", "-o", help="Email opt in", required=False, default=True)
@click.option("--all", "-a", help="RSVP for all events", required=False, is_flag=True)
def rsvp_event_command(email_opt_in: bool, all: bool):
    """RSVP for an event"""

    if (config.groups == None or len(config.groups) == 0):
        click.echo("RSVP failed, no groups selected in config", err=True)
        return

    groups: list[Group] | None = get_groups()

    if groups == None:
        click.echo("RSVP failed, no groups found", err=True)
        return

    total_groups = len(groups)
    total_eligible_groups = 0
    total_events = 0
    total_eligible_events = 0
    total_rsvp = 0

    for group in groups:

        if (group.id not in config.groups):
            logger.debug(f"Skipping group {group.urlIdentifier} because it is not selected in config")
            continue

        total_eligible_groups += 1
        events = get_group_events(group)

        if events == None:
            logger.warning(f"Failed to get events for group: {group.name}")
            click.echo(f"Failed to get events for group: {group.name}", err=True)
            continue

        for event in events:
            total_events += 1

            if (event.rsvpOpen == False):
                logger.info(f"Skipping event {event.title} because RSVP is not open")
                continue
                
            if (event.youGoing == True):
                logger.info(f"Skipping event {event.title} because you have already RSVPed to it")
                continue

            if (config.conditions.satisfy_conditions(event) == False):
                logger.info(f"Skipping event {event.title} because it does not satisfy configured conditions")
                continue
                
            total_eligible_events += 1

            try:
                rsvp = rsvp_event(event.id, getattr(event.venue, 'id', 'Online'), email_opt_in)

                if rsvp == None:
                    logger.error(f"Failed RSVPing to event {event.title}")
                    continue;
                
                total_rsvp += 1
                logger.info(f"Succesfully RSVPed to event {event.title} showing at {event.startTime} at {getattr(event.venue, 'name', 'Online')}")
            except Exception as e:
                import pdb
                pdb.set_trace()
                logger.error(f"Error RSVPing to event {event.title}: {e}")
    
    click.echo(f"Total groups: {total_groups}")
    click.echo(f"Total eligible groups: {total_eligible_groups}")
    click.echo(f"Total events: {total_events}")
    click.echo(f"Total eligible events: {total_eligible_events}")
    click.echo(f"RSVPed events count: {total_rsvp}")



@click.group()
@click.option("--log-level", "-l", help="Select Log Level", required=False, default="warn")
def main(log_level: str):

    logger.remove()
    if log_level == "debug":
        logger.add(sys.stdout, level="DEBUG")
    elif log_level == "info":
        logger.add(sys.stdout, level="INFO")
    elif log_level == "warn":
        logger.add(sys.stdout, level="WARNING")
    elif log_level == "error":
        logger.add(sys.stdout, level="ERROR")
    else:
        logger.add(sys.stdout, level="WARNING")

main.add_command(get_groups_command)
main.add_command(get_groups_events_command)
main.add_command(rsvp_event_command)
main.add_command(config_command)

if __name__ == "__main__":
    main()