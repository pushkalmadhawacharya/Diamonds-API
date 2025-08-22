import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import random
from API.schemas import Player
from SRC.bots import (
    RandomBot, GreedyBot, ConservativeBot,
    MirrorBot, MirrorThenBluffBot,
    PointAwareBot, ProbabilisticBot, MatchOrBeatBot
)
from SRC.ranks import rank_value


class DiamondsGame:
    def __init__(self, players: list[Player]):
        """
        players: list of Player objects
        """
        self.players = players
        self.diamonds = list(range(1, 14))  # Diamonds worth 1–13
        self.history = []

    def play_round(self, diamond_value: int):
        bids = {}

        for player in self.players:
            bid = player.choose_bid(diamond_value)
            player.hand.remove(bid)
            bids[player.name] = rank_value(bid)

        max_bid = max(bids.values())
        winners = [p for p, b in bids.items() if b == max_bid]

        if len(winners) == 1:
            # Single winner gets full diamond value
            for player in self.players:
                if player.name == winners[0]:
                    player.score += diamond_value
            result = f"Diamond {diamond_value}: {bids}, Winner: {winners[0]}"
        else:
            # Tie → split diamond value
            share = diamond_value / len(winners)
            for player in self.players:
                if player.name in winners:
                    player.score += share
            result = f"Diamond {diamond_value}: {bids}, Tie among {winners}, Each gets {share:.1f}"

        self.history.append(result)
        self.diamonds.remove(diamond_value)

    def play_game(self):
        random.shuffle(self.diamonds)
        while self.diamonds:
            diamond = self.diamonds[0]
            self.play_round(diamond)

    def save_results(self, filename="results.txt"):
        with open(filename, "w") as f:
            f.write("=== Round History ===\n")
            for line in self.history:
                f.write(line + "\n")
            f.write("\n=== Final Scores ===\n")
            for player in sorted(self.players, key=lambda p: -p.score):
                bot_type = f" ({player.bot.__class__.__name__})" if player.bot else ""
                f.write(f"{player.name}{bot_type}: {player.score}\n")
