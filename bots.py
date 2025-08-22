from typing import Protocol, Iterable
import random
from SRC.ranks import rank_value


class Bot(Protocol):
    def choose_bid(self, *, hand: Iterable[str], diamond_value: int) -> str:
        ...


class RandomBot:
    def choose_bid(self, *, hand: Iterable[str], diamond_value: int) -> str:
        return random.choice(list(hand))


class GreedyBot:
    def choose_bid(self, *, hand: Iterable[str], diamond_value: int) -> str:
        return max(hand, key=lambda c: rank_value(c))


class ConservativeBot:
    def choose_bid(self, *, hand: Iterable[str], diamond_value: int) -> str:
        return min(hand, key=lambda c: rank_value(c))


class MirrorBot:
    def choose_bid(self, *, hand: Iterable[str], diamond_value: int) -> str:
        # If exact match exists, use it, otherwise nearest card
        if str(diamond_value) in hand:
            return str(diamond_value)
        return min(hand, key=lambda c: abs(rank_value(c) - diamond_value))


class MirrorThenBluffBot:
    def choose_bid(self, *, hand: Iterable[str], diamond_value: int) -> str:
        if str(diamond_value) in hand:
            if random.random() < 0.5:
                return str(diamond_value)
            else:
                return min(hand, key=lambda c: rank_value(c))
        return min(hand, key=lambda c: abs(rank_value(c) - diamond_value))


class PointAwareBot:
    def choose_bid(self, *, hand: Iterable[str], diamond_value: int) -> str:
        sorted_hand = sorted(hand, key=lambda c: rank_value(c))
        if diamond_value <= 5:
            return sorted_hand[0]
        elif diamond_value <= 10:
            return sorted_hand[len(sorted_hand) // 2]
        else:
            return sorted_hand[-1]


class ProbabilisticBot:
    def choose_bid(self, *, hand: Iterable[str], diamond_value: int) -> str:
        if random.random() < 0.7:
            return max(hand, key=lambda c: rank_value(c))
        return random.choice(list(hand))


class MatchOrBeatBot:
    def choose_bid(self, *, hand: Iterable[str], diamond_value: int) -> str:
        int_hand = sorted([rank_value(c) for c in hand])

        if diamond_value in int_hand:
            return str(diamond_value)
        higher_cards = [c for c in int_hand if c > diamond_value]
        if higher_cards:
            return str(higher_cards[0])
        return str(int_hand[0])
