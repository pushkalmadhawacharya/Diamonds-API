import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from SRC.ranks import RANKS


class Player:
    
    def __init__(self, name: str, hand: Optional[List[str]] = None, bot=None):
        self.name = name
        self.hand = hand if hand is not None else RANKS.copy()
        self.score: float = 0
        self.bot = bot  

    def choose_bid(self, diamond_value: int) -> str:
      
        if self.bot:
            return self.bot.choose_bid(hand=self.hand, diamond_value=diamond_value)
        return self.hand[0]


class PlayerCreate(BaseModel):
    player_id: str = Field(..., description="Unique ID for the player")
    is_bot: bool = False
    bot_kind: Optional[
        Literal["random", "greedy", "conservative", "mirror",
                "mirror_bluff", "point_aware", "probabilistic", "match"]
    ] = None


class GameCreate(BaseModel):
    game_id: str = Field(..., description="Unique ID for the game")
    players: List[PlayerCreate]


class PlayerStatus(BaseModel):
    player_id: str
    score: float
    is_active: bool
    is_bot: bool
    bot_kind: Optional[str] = None


class GameStatus(BaseModel):
    game_id: str
    state: Literal["waiting", "running", "finished", "abandoned"]
    players: List[PlayerStatus]


class GameResult(BaseModel):
    game_id: str
    winner: Optional[str] = None
    scores: dict


class GameAction(BaseModel):
    action: Literal["start", "abandon"]
