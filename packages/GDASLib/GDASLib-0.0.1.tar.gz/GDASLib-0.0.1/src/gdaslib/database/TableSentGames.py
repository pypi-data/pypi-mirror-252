from dataclasses import dataclass

@dataclass
class TableSentGames:
    """ the information for the games already sent"""
    gameid: int
    championship: str
    stage: str
    filename: str
    email: str
    sent: bool