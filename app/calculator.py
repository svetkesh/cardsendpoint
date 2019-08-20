#!flask/bin/python
from collections import Counter

VALUES_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def max_value(cards, reverse=False, second=False):
    """Calculate maximum value of cards (minimum if reverse=True)"""
    try:
        indexes = [VALUES_ORDER.index(c) for c in cards]
        # sorted(indexes, reverse=reverse)
        list.sort(indexes, reverse=reverse)
        print(indexes)
        if not second:
            return VALUES_ORDER[indexes[-1]]
        else:
            return VALUES_ORDER[indexes[-2]]
    except Exception:
        # hand = hand.split(",")
        raise Exception(f"ERROR not a valid format for cards: {cards}")

def verbose(coded_values):
    try:
        # {"rank": rank, "max_card": max_card, "second_value": second_value}

        rank = coded_values["rank"]
        max_card = coded_values["max_card"]
        second_value = coded_values["second_value"]

        DICT_SUITS = {
            "C": "clubs",
            "D": "dimonds",
            "H": "hearts",
            "S": "spides",

        }
        DICT_VALS = {
            "2": "two", "3": "three", "4": "four", "5": "five",
            "6": "six", "7": "seven", "8": "eight", "9": "nine",
            "10": "ten", "J": "jack", "Q": "queen", "K": "king", "A": "ace"
        }
        DICT_RANKS = {
            0: "high card is ",
            1: "pair of ",
            2: "set of ",
            0: "high card is ",
        }

        if rank == 0:
            readable_value = f"high card is {DICT_VALS[max_card]}"
        elif rank == 1:
            readable_value = f"pair of {DICT_VALS[max_card]}s with highest next {DICT_VALS[second_value]}"
        elif rank == 2:
            readable_value = f"two pairs of {DICT_VALS[max_card]}s and {DICT_VALS[second_value]}"
        elif rank == 3:
            readable_value = f"three of a kind {DICT_VALS[max_card]}s with {DICT_VALS[second_value]}"
        elif rank == 4:
            readable_value = f"straight from {DICT_VALS[max_card]}"
        elif rank == 5:
            readable_value = f"flush starts from {DICT_VALS[max_card]}"
        elif rank == 6:
            readable_value = f"full house {DICT_VALS[max_card]}s with {DICT_VALS[second_value]}s"
        elif rank == 7:
            readable_value = f"four of a kind {DICT_VALS[max_card]}s with {DICT_VALS[second_value]}"
        else:
            readable_value = f"straight flush or even royal flush, you win for sure except 1/1317239 chance."

        return readable_value


    except Exception as e:
        return {"result": str(e)}



def calculate(hand):
    """Calculate poker cards wining combination rank, higher - better and higher card

    Accepts cards in format
    'XY' , where X is suit
         'Y' stands for card value, could be any in
            "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "D", "K", "A"

    For given request:

    POST 127.0.0.1:5005/api/v1.0/hands
    {
        "hand": ["DK", "CA", "D7", "D7", "CK"]
    }

    returns:
    {
      "hand": {
        "max_card": "K",
        "rank": 2,
        "second_value": "7"
      }
    }

    where rank 1 stands for 'pair of'
    and A for ACE

    """
    # print(hand)
    try:
        # report = {}
        result = 0
        rank = 0

        if isinstance(hand, str):
            print(f"DBG processing string hand: {type(hand), hand}")
            hand = hand.split(",")

        if not isinstance(hand, list):
            # hand = hand.split(",")
            raise Exception(f"ERROR not a valid format, expected list, given: {type(hand)}")

        if len(hand) != 5:
            raise Exception(f"ERROR not a valid format, expected 5 cards, given: {len(hand)}")

        cards = [(c[0], c[1:]) for c in hand]
        # print(f"cards: {cards}")
        card_values = [c[1] for c in cards]
        # print(f"card_values: {card_values}")
        card_suits = [c[0] for c in cards]
        # print(f"card_suits: {card_suits}")

        # max card
        max_card = max_value(card_values)
        print(f"max_card: {max_card}")

        min_card = max_value(card_values, reverse=True)
        print(f"min_card: {min_card}")

        # using Counter
        two_most_often_values = Counter(card_values).most_common(2)
        print(two_most_often_values[0])
        print(two_most_often_values[1])

        two_most_often_suits = Counter(card_suits).most_common(2)
        print(two_most_often_suits[0])

        most_0 = two_most_often_values[0][1]
        most_1 = two_most_often_values[1][1]


        if most_0 == 2:
            rank = 1    # pair
        if most_0 == 2 and most_1 == 2:
            rank = 2    # two pairs
        if most_0 == 3:
            rank = 3    # three of a kind
        if VALUES_ORDER.index(max_card) - VALUES_ORDER.index(min_card) == 5:
            max_card = two_most_often_values[0][0]
            rank = 4    # Straight
        if len(set(card_suits)) == 1:
            rank = 5    # flush
            max_card = two_most_often_values[0][0]
        if most_0 == 3 and most_1 == 2:
            rank = 6    # full house
        if most_0 == 4:
            rank = 7    # four of a kind
        # ...
        if most_0 > 1:
            max_card = two_most_often_values[0][0]
            if most_1 >1:
                second_value = two_most_often_values[1][0]
            else:
                second_value = max_value(card_values, second=True)

        print(f"calculate found:{rank}")

        coded_values = {"rank": rank, "max_card": max_card, "second_value": second_value}
        readable_value = verbose(coded_values)

        return {"result": readable_value}

    except Exception as e:
        return {"result": str(e)}


def process_hands(hands):
    """Espect dictionary of players with hands"""
    try:
        report = {}
        for player in hands:
            report[player] = calculate(hands[player])
        return report
    except Exception as e:
        raise Exception(f"ERROR while processing hands: {type(e), e}")
