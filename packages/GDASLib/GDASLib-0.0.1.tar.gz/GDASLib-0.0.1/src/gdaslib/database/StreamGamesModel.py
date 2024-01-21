from dataclasses import dataclass
import datetime
import json

@dataclass
class StreamGamesModel:
    """ the model for the stream games """
    stream_game_id: int = None
    sg_datetime: datetime = None

    @staticmethod
    def from_data(input_data):
        """ converts string to object, string must be in json format """
        input_json = json.loads(input_data)
        return StreamGamesModel(input_json["stream_game_id"] if "stream_game_id" in input_json else None,
                                input_json["sg_datetime"] if "sg_datetime" in input_json else None)
