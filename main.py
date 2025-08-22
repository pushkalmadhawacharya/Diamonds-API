import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from API.schemas import GameCreate, GameStatus, GameResult, GameAction, Player
from SRC.game import DiamondsGame
from SRC.bots import (
    RandomBot, GreedyBot, ConservativeBot,
    MirrorBot, MirrorThenBluffBot,
    PointAwareBot, ProbabilisticBot, MatchOrBeatBot
)

app = FastAPI(title="Diamonds API Service")

games = {}

BOT_MAP = {
    "random": RandomBot,
    "greedy": GreedyBot,
    "conservative": ConservativeBot,
    "mirror": MirrorBot,
    "mirror_bluff": MirrorThenBluffBot,
    "point_aware": PointAwareBot,
    "probabilistic": ProbabilisticBot,
    "match": MatchOrBeatBot,
}


@app.post("/games/create")
def create_game(game_data: GameCreate):
    if game_data.game_id in games:
        raise HTTPException(status_code=400, detail="Game ID already exists")

    players = []
    for p in game_data.players:
        bot = BOT_MAP[p.bot_kind]() if p.is_bot and p.bot_kind else None
        players.append(Player(name=p.player_id, bot=bot))

    game = DiamondsGame(players)
    games[game_data.game_id] = {"game": game, "state": "waiting"}

    return {"message": f"Game {game_data.game_id} created with {len(players)} players"}


@app.post("/games/{game_id}/action")
def game_action(game_id: str, action: GameAction):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    entry = games[game_id]
    game = entry["game"]

    if action.action == "start":
        if entry["state"] != "waiting":
            raise HTTPException(status_code=400, detail="Game already started or finished")
        game.play_game()
        entry["state"] = "finished"
        return {"message": f"Game {game_id} finished"}
    elif action.action == "abandon":
        entry["state"] = "abandoned"
        return {"message": f"Game {game_id} abandoned"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")


@app.get("/games/{game_id}/status", response_model=GameStatus)
def get_status(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    entry = games[game_id]
    game = entry["game"]

    players_status = []
    for p in game.players:
        players_status.append({
            "player_id": p.name,
            "score": p.score,
            "is_active": len(p.hand) > 0,
            "is_bot": p.bot is not None,
            "bot_kind": p.bot.__class__.__name__ if p.bot else None
        })

    return {
        "game_id": game_id,
        "state": entry["state"],
        "players": players_status
    }


@app.get("/games/{game_id}/result", response_model=GameResult)
def get_result(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    entry = games[game_id]
    if entry["state"] not in ["finished", "abandoned"]:
        raise HTTPException(status_code=400, detail="Game still running or not started")

    game = entry["game"]
    scores = {p.name: p.score for p in game.players}
    winner = max(scores, key=scores.get) if entry["state"] == "finished" else None

    return {
        "game_id": game_id,
        "winner": winner,
        "scores": scores
    }
@app.get("/")
def root():
    return {"message": "Diamond Game API is running 🚀"}