from dataclasses import dataclass
import json
from os import name
from src.models.event import EventRsvpConditions
from loguru import logger

@dataclass
class MeetupConfig:

    groups: list[str]
    conditions: EventRsvpConditions

    def __init__(self) -> None:
        self.groups = []
        self.conditions = EventRsvpConditions()
        self.__load__config()
        pass

    def __load__config(self) -> None:
        try:
            with open('config.json') as f:
                jsonConfig = json.load(f)

                if len(jsonConfig.keys()) == 0:
                    logger.warning("Config file is empty")
                    return

                self.groups = jsonConfig.get('groups', [])

                if 'conditions' in jsonConfig:
                    self.conditions = EventRsvpConditions.from_json(jsonConfig.get('conditions'))
                else:
                    logger.debug("No conditions found in config file")

        except FileNotFoundError:
            logger.warning("Config file not found")
            return
        except json.JSONDecodeError:
            logger.error("Error parsing config file")
        except Exception as e:
            logger.error(f"Error loading config file: {e}")


    def save(self) -> None:
        with open('config.json', 'w') as f:
            jsonConfig = {
                'groups': self.groups,
                'conditions': self.conditions .__dict__ if self.conditions is not None else None
            }
            json.dump(jsonConfig, f)