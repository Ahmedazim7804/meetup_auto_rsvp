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
    creatorId: str | None
    eventHosts: list[str]
    feeSettings: Any
    venue: EventVenue | None
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

        eventPhoto = None
        if (json.get('featuredEventPhoto', {})) is not None:
            eventPhoto = json.get('featuredEventPhoto', {}).get('source', None)

        eventHosts = []
        if (rawEventHosts := json.get('eventHosts', [])) is not None:
            for host in rawEventHosts:
                eventHosts.append(host.get('memberId'))
        
        creatorId = None
        if (creator := json.get('creatorId', {})) is not None:
            creatorId = creator.get('id', None)
        
        venue = None
        if (rawVenue := json.get('venue', {})) is not None:
            venue = EventVenue(
                id=rawVenue['id'],
                name=rawVenue['name'],
                address=rawVenue['address'],
                city=rawVenue['city'],
                state=rawVenue.get('state', None)
            )
        
        return Event(
            id=json['id'],
            title=json['title'],
            eventUrl=json['eventUrl'],
            description=json['description'],
            creatorId=creatorId,
            eventHosts=json['eventHosts'],
            feeSettings=json['feeSettings'],
            
            venue=venue,

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



