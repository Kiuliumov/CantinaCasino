class Utils:

    SUITS = ["♠", "♥", "♦", "♣"]
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    VALUES = {
        "A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10
    }

    @staticmethod
    def draw_card():
        return random.choice(RANKS), random.choice(SUITS)

    @staticmethod
    def hand_value(hand):
        value = sum(VALUES[r] for r, _ in hand)
        aces = sum(1 for r, _ in hand if r == "A")
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    @staticmethod
    def format_hand(hand):
        return " ".join(f"{r}{s}" for r, s in hand)
