#!flask/bin/python
from collections import Counter


VALUES_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "D", "K", "A"]


def max_value(cards, reverse=False):
    """Calculate maximum value of cards (minimum if reverse=True)"""
    try:
        indexes = [VALUES_ORDER.index(c) for c in cards]
        # sorted(indexes, reverse=reverse)
        list.sort(indexes, reverse=reverse)
        print(indexes)
        return VALUES_ORDER[indexes[0]]
    except Exception:
        # hand = hand.split(",")
        raise Exception(f"ERROR not a valid format for cards: {cards}")


def calculate(hand):
    """Calculate poker cards wining combination rank, higher - better and higher card"""
    # print(hand)
    try:
        # report = {}
        result = 0
        rank = 0

        cards = [(c[0], c[1:]) for c in hand]
        print(f"cards: {cards}")
        card_values = [c[1] for c in cards]
        print(f"card_values: {card_values}")
        card_m = [c[0] for c in cards]
        print(f"card_m: {card_m}")

        if not isinstance(hand, list):
            # hand = hand.split(",")
            raise Exception(f"ERROR not a valid format, expected list, given: {type(hand)}")
        if len(hand) != 5:
            raise Exception(f"ERROR not a valid format, expected 5 cards, given: {len(hand)}")

        # max card
        max_card = max_value(card_values, reverse=True)
        print(f"max_card: {max_card}")

        min_card = max_value(card_values)
        print(f"min_card: {min_card}")

        # using Counter
        two_most_often_values = Counter(card_values).most_common(2)
        print(two_most_often_values[0])
        print(two_most_often_values[1])

        two_most_often_m = Counter(card_m).most_common(2)
        print(two_most_often_m[0])

        most_m = two_most_often_m[0][1]

        most_0 = two_most_often_values[0][1]
        most_1 = two_most_often_values[1][1]

        if most_0 == 2:
            rank = 1    # pair
        if most_0 == 3:
            rank = 2    # set
        if most_0 == 2 and most_1 == 2:
            rank = 3    # two pairs

        if most_m == 5:
            rank = 4    # flash

        if VALUES_ORDER.index(max_card) - VALUES_ORDER.index(min_card) == 5:
            rank = 5    # street

        if most_0 == 3 and most_1 == 2:
            rank = 6    # house

        # ...

        print(f"calculate found:{rank}")

        return {"rank": rank, "max_card": max_card}

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

