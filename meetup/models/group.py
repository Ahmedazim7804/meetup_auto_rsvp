from dataclasses import dataclass
from typing import Any, Dict 

@dataclass()
class Group:
    id: int
    name: str
    link: str
    city: str
    urlIdentifier: str
    country: str
    state: str | None
    timezone: str | None
    groupPhoto: str | None
    organizerId: str | None

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'Group':
        groupPhoto : str | None = None

        try:
            groupPhoto = json.get('groupPhoto').__getattribute__('baseUrl') + json.get('groupPhoto').__getattribute__('id')
        except:
            pass

        return Group(
            id=json['id'],
            name=json['name'],
            link=json['link'],
            city=json['city'],
            urlIdentifier=json['urlname'],
            state=json.get('state', None),
            country=json['country'],
            timezone=json.get('timezone', None),
            groupPhoto=groupPhoto,
            organizerId=json.get('organizer', {}).get('id', None)
        )

