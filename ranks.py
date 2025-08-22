RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
RANK_TO_VALUE = {"A":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13}
VALUE_TO_RANK = {v:k for k,v in RANK_TO_VALUE.items()}

def rank_value(rank: str) -> int:

    v = RANK_TO_VALUE.get(rank)
    if v is None:
        raise ValueError(f"invalid rank: {rank}")
    return v