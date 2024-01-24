from dataclasses import dataclass, InitVar, field
from .team import Team
from datetime import datetime
from dateutil import parser


@dataclass
class Game:
    game_data: InitVar[dict]
    game_id: str = field(init=False)
    winner: int = field(init=False, default=-1)  # Top = 0, Bottom = 1
    created_at: datetime = field(init=False, default=None)

    def __post_init__(self, game_data: dict):
        if created_at := game_data.get("createdAt"):
            self.created_at = parser.isoparse(created_at)
        self.game_id = game_data.get("_id", None)
        stats = game_data.get("stats")
        if stats:
            if stats["top"]["winner"]:
                self.winner = 0
            elif stats["bottom"]["winner"]:
                self.winner = 1


@dataclass
class Match:
    match_data: InitVar[dict]
    # attributes
    top: Team
    bottom: Team
    id: str = field(init=False, default="")
    games: list = field(init=False, default_factory=list)
    created_at: datetime = field(init=False, default=None)
    top_win: int = field(init=False, default=0)
    bottom_win: int = field(init=False, default=0)

    def __post_init__(self, match_data: dict):
        self.id = match_data.get("_id")
        if created_at := match_data.get("createdAt"):
            self.created_at = parser.isoparse(created_at)
        if "stats" in match_data:
            for g in match_data.get("stats", []):
                self.games.append(Game(g))
            for game in self.games:
                if game.winner == 0:
                    self.top_win += 1
                elif game.winner == 1:
                    self.bottom_win += 1
        else:
            self.top_win = match_data.get("top", {}).get("score", 0)
            self.bottom_win = match_data.get("bottom", {}).get("score", 0)


    @property
    def valid_games(self):
        valid = Team
        for g in self.games:
            if g.winner == -1:
                valid = field()
        return valid
