from dataclasses import dataclass
from typing import Any, Dict 

@dataclass()
class EventRsvpConditions:
    isPaid: bool = False
    isOnline: bool = True
    minNumAttendees: int = 0

    @staticmethod
    def from_json(json: dict[str, Any]) -> 'EventRsvpConditions':
        return EventRsvpConditions(
            isPaid=json['isPaid'],
            isOnline=json['isOnline'],
            minNumAttendees=json['minNumAttendees']
        )
    
    def satisfy_conditions(self, event: 'Event') -> bool:
        # If the event is paid and the user does not want to go to paid event, return False
        if (not self.isPaid) and event.feeSettings is not None:
            return False

        # If the event is online and the user does not want to go to online event, return False
        if event.isOnline and not self.isOnline:
            return False

        # If the event does not have enough attendees, return False
        if event.numAttendees < self.minNumAttendees:
            return False

        return True




@dataclass()
class EventVenue:
    id: str
    name: str
    address: str
    city: str
    state: str | None


@dataclass()
class Event:
    id: str
    title: str
    eventUrl: str
    description: str | None
    creatorId: str
    eventHosts: list[str]
    feeSettings: Any
    venue: EventVenue
    createdTime: str
    startTime: str
    endTime: str
    numAttendees: int
    youGoing: bool
    isOnline: bool
    status: str
    eventPhoto: str | None
    rsvpOpen : bool

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'Event':
        eventPhoto = json.get('featuredEventPhoto', {}).get('source', None)

        rawEventHosts = json.get('eventHosts', [])
        eventHosts = []
        for host in rawEventHosts:
            eventHosts.append(host.get('memberId'))
        
        return Event(
            id=json['id'],
            title=json['title'],
            eventUrl=json['eventUrl'],
            description=json['description'],
            creatorId=json.get('creatorId', {}).get('id'),
            eventHosts=json['eventHosts'],
            feeSettings=json['feeSettings'],

            venue=EventVenue(
                id=json['venue']['id'],
                name=json['venue']['name'],
                address=json['venue']['address'],
                city=json['venue']['city'],
                state=json['venue'].get('state', None)
            ),

            createdTime=json['createdTime'],
            startTime=json['dateTime'],
            endTime=json['endTime'],

            numAttendees=json.get('going', {}).get('totalCount', 0),
            youGoing=json.get('isAttending', False),
            isOnline=json.get('isOnline', False),
            status=json['status'],
            eventPhoto=eventPhoto,
            rsvpOpen=not json.get('rsvpSettings', {}).get('rsvpsClosed', True)
        )



