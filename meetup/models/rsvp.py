from dataclasses import dataclass
from typing import Dict 

@dataclass()
class Rsvp:
    id: str
    status: str
    guestsCount: int
    payStatus: str | None

    @staticmethod
    def from_json(json: Dict[str, any]) -> 'Rsvp':

        return Rsvp(
            id=json['id'],
            status=json['status'],
            guestsCount=json['guestsCount'],
            payStatus=json.get('payStatus', None)
        )
