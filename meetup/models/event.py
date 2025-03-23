from dataclasses import dataclass
from typing import Any, Dict 

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



