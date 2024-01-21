from dataclasses import dataclass

@dataclass
class GamesGamesModel:
    """ direct connection to the games table """
    id: int
    start_time: str
    championship: str
    number: str
    echelon: str
    current_period: str
    team1_fouls: int
    team2_fouls: int
    team1_score: int
    team2_score: int
    current_time: str
    stream_key: str
    stream_url: str
    team1_id: int
    team2_id: int
    team1_timeout: int
    team2_timeout: int
    timeout_time: str
    shoot_clock: str
    total_periods: int
    game_clock: bool
    end_time: str
